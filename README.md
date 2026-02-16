# FRD — Ferramenta de Redes e Segurança

FRD é uma ferramenta em Python focada em **redes, endereçamento IP e segurança**, com interface de linha de comando (CLI), arquitetura modular e testes automatizados. É uma ferramenta de estudo, a idéia era fazer um sistema completo com github, readme detalhado, etc., para fins educacionais. Como segurança e redes são áreas que gosto e estudo muito, resolvi focar nelas. O sistema esta em constante evolução e pode apresentar erros, o que é natural, pois como já dito é fonte de estudos. 
Espero que gostem e façam bom uso.


O README foi escrito para que **qualquer pessoa** consiga instalar e executar o projeto — inclusive quem nunca criou `venv` ou usou `pip` antes.

> 🚧 Projeto voltado para estudo de Segurança. Pode evoluir, parar ou mudar de escopo.

---

## ✨ Principais características

- CLI moderna baseada em **Typer**
- Estrutura organizada em `src/`
- Módulos independentes e testáveis
- Suporte a **IPv4**, **IPv6**, **DNS**, **Scan TCP** e **Web auditing**
- Testes automatizados com **pytest** (unitários e integração)
- Compatível com **Windows, macOS e Linux**

---

## 📁 Estrutura do projeto

```
frd/
├── src/
│   └── frd/
│       ├── cli.py
│       ├── ipv4/
│       ├── ipv6/
│       ├── dns/
│       ├── scan/
│       └── web/
├── tests/
├── pyproject.toml
├── run.sh
└── README.md
```

---

## 📚 Conceitos rápidos (para iniciantes)

- **Python**: linguagem usada no FRD.
- **pip**: ferramenta que instala bibliotecas/projetos Python.
- **venv**: “ambiente virtual” que isola as dependências do FRD para não misturar com outros projetos.

---

## ✅ Pré-requisitos

- Python **3.10+**
- Git (opcional, mas recomendado)

Verifique se o Python está instalado:

- Windows:
```powershell
python --version
```

- macOS/Linux:
```bash
python3 --version
```

---

## ⬇️ Baixar o projeto

Com Git:

```bash
git clone https://github.com/SEU_USUARIO/frd.git
cd frd
```

Ou baixe o ZIP pelo GitHub e extraia, então entre na pasta do projeto.

---

## 🧰 Instalação (venv + pip + FRD)

### Windows (PowerShell)

1) Criar e ativar o venv:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

> Se der erro de política do PowerShell, execute **como administrador**:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

2) Atualizar pip e instalar o FRD:
```powershell
python -m pip install -U pip
pip install -e .
```

3) Testar:
```powershell
frd --help
```

Se o comando `frd` não aparecer, use:
```powershell
python -m frd.cli --help
```

---

### macOS / Linux

1) Criar e ativar o venv:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Atualizar pip e instalar o FRD:
```bash
python -m pip install -U pip
pip install -e .
```

3) Rodar:
```bash
frd --help
```

Se o entrypoint `frd` não estiver disponível, use o script auxiliar:

```bash
chmod +x run.sh
./run.sh --help
```

---

## 🚀 Uso

### Ajuda geral
```bash
frd --help
```

### Ajuda por módulo
```bash
frd net --help
frd dns --help
frd scan --help
frd web --help
```

---

## 🧭 Módulos e exemplos

### 📡 Net (IPv4 / IPv6)

```bash
frd net ipv4-info 192.168.0.1/24
frd net ipv6-info 2001:db8::1
frd net ipv6-expand 2001:db8::1
frd net ipv6-reverse 2001:db8::1
```

### 🌐 DNS

```bash
frd dns resolve google.com
```

> Em algumas redes corporativas, DNS por UDP/53 pode ser bloqueado.

### 🔍 Scan (TCP)

```bash
frd scan tcp 8.8.8.8 --ports 53
frd scan tcp 8.8.8.8 --ports 22,53,443
```

### 🌍 Web (auditoria HTTP)

Checagem explícita de paths 
> ⚠️ Não é crawling e nem brute force.

```bash
frd web check https://example.com --paths-file paths.txt
```

Exemplo de `wordlist.txt`:
```text
/
robots.txt
sitemap.xml
admin/
uploads/
css/
```

Mais exemplos:
```bash
frd web check https://example.com --paths-file paths.txt --include 200,301,302,401,403
frd web check https://example.com --paths-file paths.txt --method HEAD
frd web check https://example.com --paths-file paths.txt --json
```

---

## 🧪 Testes

```bash
python -m pytest -q
python -m pytest
python -m pytest --markers
```

---

## 🧹 Qualidade (Lint)

```bash
ruff check .
```

---

## 📄 Licença

MIT
