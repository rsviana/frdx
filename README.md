# FRD — Ferramenta de Redes e Segurança

FRD é uma ferramenta em Python focada em **redes, endereçamento IP e segurança**, com interface de linha de comando (CLI), arquitetura modular e testes automatizados.

O projeto foi desenhado para ser **previsível e extensível**, servindo tanto para uso prático quanto para estudo.

> Esse projeto ainda esta em evolução e testes 

---

## ✨ Principais características

- CLI moderna baseada em **Typer**
- Estrutura organizada em `src/`
- Suporte completo a **IPv4** e **IPv6**
- Módulos independentes e testáveis
- Testes unitários com **pytest**
- Compatível com **Windows, macOS e Linux**
- Sem dependência de rede para testes unitários

---

## 📁 Estrutura do projeto

```
frd/
├── src/
│   └── frd/
│       ├── cli/
│       │   └── cli.py
│       ├── ipv4/
│       ├── ipv6/
│       └── dns/
├── tests/
│   ├── ipv4/
│   ├── ipv6/
│   └── dns/
├── pyproject.toml
└── README.md
```

---

## 🚀 Uso

### Executando no Windows

```bash
python -m frd.cli
```

### Executando no macOS / Linux

```bash
./run.sh
```

Ou diretamente:

```bash
python -m frd.cli
```

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

### Testes de integração

Os testes de DNS são marcados como `integration`.

Por padrão, eles são ignorados:

```toml
addopts = ["-m", "not integration"]
```

Para rodar tudo:

```bash
python -m pytest
```

---

## 🧠 Filosofia do projeto

- Código claro > código mágico
- CLI previsível e consistente
- Funções pequenas e testáveis
- IPv6 tratado como cidadão de primeira classe
- Crescimento incremental e bem testado
- Para TODOS usarem e contribuirem

---

## 📌 Roadmap (curto prazo)

- Evolução do módulo `ipv6-subnets`
- Comandos auxiliares IPv6:
  - `ipv6-range`
  - `ipv6-contains`
  - `ipv6-summarize`
- Padronização de saída (`--json`)

---

## 📄 Licença

MIT
