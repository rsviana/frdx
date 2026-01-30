# FRD — Ferramenta de Redes e Segurança

FRD é uma ferramenta em Python focada em **redes, endereçamento IP e segurança**, com interface de linha de comando (CLI), arquitetura modular e testes automatizados.

O projeto foi desenhado para ser **previsível, auditável e extensível**, servindo tanto para uso prático quanto para estudo.

> 🚧 Projeto em evolução contínua

---

## ✨ Principais características

- CLI moderna baseada em **Typer**
- Estrutura organizada em `src/`
- Módulos independentes e testáveis
- Suporte a **IPv4**, **IPv6**, **DNS**, **Scan TCP** e **Web auditing**
- Testes unitários e de integração com **pytest**
- Compatível com **Windows, macOS e Linux**
- Núcleo funcional testável sem dependência de rede externa

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
│   ├── ipv4/
│   ├── ipv6/
│   ├── dns/
│   ├── scan/
│   └── web/
├── pyproject.toml
└── README.md
```

---

## 🚀 Uso

### Executando no Windows

```bash
frd --help
```

Ou diretamente:

```bash
python -m frd.cli
```

### Executando no macOS / Linux

```bash
./run.sh
```

---

## 🧭 Visão geral dos módulos

### 📡 Net (IPv4 / IPv6)

```bash
frd net --help
```

Exemplos:

```bash
frd net ipv4-info 192.168.0.1/24
frd net ipv6-info 2001:db8::1
frd net ipv6-expand 2001:db8::1
frd net ipv6-reverse 2001:db8::1
```

---

### 🌐 DNS

```bash
frd dns --help
frd dns resolve google.com
```

> Testes DNS com rede são marcados como `integration`.

---

### 🔍 Scan (TCP)

```bash
frd scan --help
```

Exemplo:

```bash
frd scan tcp 8.8.8.8 --ports 53
```

Múltiplas portas:

```bash
frd scan tcp 8.8.8.8 --ports 22,53,443
```

---

### 🌍 Web (auditoria HTTP)

Módulo dedicado para **checagem explícita de paths HTTP**, com saída em tempo real.

```bash
frd web --help
```

#### Exemplo básico

```bash
frd web check https://example.com --paths /
```

#### Usando arquivo de paths

```bash
frd web check https://example.com --paths-file paths.txt
```

Exemplo de `paths.txt`:

```text
/
robots.txt
admin/
uploads/
api/
```

#### Filtrar por status HTTP

```bash
frd web check https://example.com --paths-file paths.txt --include 200,301,302,401,403
```

#### Método HEAD (mais rápido)

```bash
frd web check https://example.com --paths-file paths.txt --method HEAD
```

#### Saída em JSON (relatório)

```bash
frd web check https://example.com --paths-file paths.txt --json
```

> O módulo **não faz crawling nem brute force**.  
> Apenas testa os paths explicitamente informados.

---

## 🌐 Comandos IPv6 disponíveis

- `ipv6-info` — informações detalhadas sobre um endereço IPv6
- `ipv6-expand` — expande IPv6 compactado
- `ipv6-reverse` — gera o reverse DNS (ip6.arpa)
- `ipv6-subnets` — gera sub-redes a partir de um prefixo IPv6 (**em evolução**)

Todos os comandos IPv6 funcionam **offline**, usando apenas a biblioteca padrão.

---

## 🧪 Testes

O projeto utiliza **pytest**.

### Executar testes unitários

```bash
python -m pytest -q
```

### Executar todos os testes (incluindo integração)

```bash
python -m pytest
```

### Ver markers disponíveis

```bash
python -m pytest --markers
```

---

## 🧠 Filosofia do projeto

- Código claro > código mágico
- CLI previsível e explícita
- Funções pequenas e testáveis
- IPv6 tratado como cidadão de primeira classe
- Ferramenta pensada para profissionais
- Crescimento incremental, validado por testes

---

## 📌 Roadmap (curto prazo)

- Evolução do módulo `ipv6-subnets`
- Novos utilitários IPv6:
  - `ipv6-range`
  - `ipv6-contains`
  - `ipv6-summarize`
- Melhorias no módulo `web`:
  - headers customizados
  - modo verbose / quiet
  - baseline e diff de auditoria
- Padronização de saída (`--json`)

---

## 📄 Licença

MIT
