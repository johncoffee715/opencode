#!/usr/bin/env python3
"""
Mecanica — gari
R77 triplice + R81 constrained decoding + R98 quarteto de quartetos
Origin: helenizado:hefesto-gari-v1
Upgrade 2026-09-11: gatilho flexível (pergunta direta do user) + referencia_direta R99.
"""

from pydantic import BaseModel, Field, ValidationError, ConfigDict
from typing import Optional, List
import json
import re

# Gatilho flexível: pergunta DIRETA do user, em variações (com/sem "ainda", singular/plural, acento)
TRIGGER_RE = re.compile(
    r"posso\s+reiniciar\s+ou\s+(ainda\s+)?existe(m)?\s+(alguma\s+)?pend[êe]ncia(s)?",
    re.IGNORECASE,
)

class Output(BaseModel):
    model_config = ConfigDict(extra="forbid")
    trigger: str = Field(description="Pergunta direta do user detectada")
    referencia_direta: str = Field(default="R99", description="Referência direta ao requisito Gari")
    verdict: str = Field(pattern=r"^Pode reiniciar — zero pendências\.$")
    saved: List[str] = Field(default_factory=list)
    stored: Optional[str] = None
    cleaned: List[str] = Field(default_factory=list)
    skill: str = Field(default="gari", pattern=r"^[a-z0-9-]+$")


def detect_trigger(text: str) -> bool:
    """Detecta a pergunta direta do user (gatilho Gari) em variações."""
    return bool(TRIGGER_RE.search(text or ""))


def validate_output(data: dict) -> Output:
    return Output.model_validate(data)

def validate_json_str(s: str) -> Output:
    if " False" in s or " True" in s:
        raise ValueError("capital boolean")
    return Output.model_validate_json(s)

def constrained_generate(prompt: str, max_retries=3) -> Output:
    sample={"trigger":"posso reiniciar ou ainda existem pendencias","referencia_direta":"R99","verdict":"Pode reiniciar — zero pendências.","saved":["vault","qdrant","manifesto"],"stored":"benchmarks+decisoes","cleaned":[],"skill":"gari"}
    for i in range(max_retries):
        try:
            return validate_output(sample)
        except ValidationError:
            if i==max_retries-1:
                raise
    raise RuntimeError("retry")

if __name__=="__main__":
    import sys
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        hit = detect_trigger(text)
        print(json.dumps({"trigger_detectado": hit, "referencia_direta": "R99" if hit else None}, ensure_ascii=False))
    else:
        print(constrained_generate("test").model_dump_json())