# FRD - Ferramenta de Redes e Segurança

Toolkit CLI em Python para profissionais de redes e segurança.
> Ainda melhorando...

## Instalação (modo dev)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
``` 
# 
```
frd net ipv4-info 192.168.10.0/24
frd net cidr-to-mask 26
frd net mask-to-cidr 255.255.255.0

frd dns resolve example.com --type A
frd dns reverse 8.8.8.8

frd scan tcp 127.0.0.1 --ports 22,80,443
frd diag tcp-ping example.com --port 443 --count 4
```
# Aviso
| Use recursos de varredura apenas com autorização.


---

# Como rodar agora
No root do projeto:
```
pip install -e .
frd --help
frd net ipv4-info 192.168.1.0/24
frd scan tcp 127.0.0.1 --ports 22,80,443 --json
```
