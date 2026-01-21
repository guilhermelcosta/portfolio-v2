# Portfolio v2 - Automated Resume to Markdown

Este projeto converte automaticamente seu currículo em PDF para Markdown e publica no GitHub Pages.

## 🚀 Como Funciona

### Workflow Único e Consolidado

Quando você adiciona um novo PDF de currículo na pasta `resumes/`, um único workflow é disparado:

**`Update Resume and Deploy`** (`.github/workflows/update-resume.yml`)
1. ✅ Extrai o conteúdo do PDF mais recente
2. ✅ Gera/atualiza o `index.md` preservando toda a informação
3. ✅ Faz commit das mudanças
4. ✅ Faz build do Jekyll
5. ✅ Faz deploy no GitHub Pages

Tudo em **uma única execução**, sem workflows duplicados!

## 📁 Estrutura

```
portfolio-v2/
├── .github/
│   ├── workflows/
│   │   └── update-resume.yml    # Workflow consolidado
│   └── scripts/
│       └── update_resume.py     # Script de conversão PDF → Markdown
├── resumes/
│   ├── resume-guilherme-costa-en-rev-2.pdf
│   ├── resume-guilherme-costa-en-rev-3.pdf
│   └── ...                      # Novos PDFs aqui
├── _config.yml                  # Configuração Jekyll
├── index.md                     # Currículo em Markdown (gerado automaticamente)
└── last_processed.txt           # Controle de versão processada
```

## 🎯 Como Usar

### Atualizar seu Currículo

1. Crie um novo PDF seguindo o padrão: `resume-guilherme-costa-en-rev-X.pdf`
   - Incremente o número da revisão (rev-3, rev-4, etc.)

2. Adicione na pasta `resumes/`:
   ```bash
   cp ~/Downloads/novo-curriculo.pdf resumes/resume-guilherme-costa-en-rev-X.pdf
   ```

3. Commit e push:
   ```bash
   git add resumes/
   git commit -m "Add resume rev-X"
   git push
   ```

4. ✨ **Pronto!** O workflow vai:
   - Processar o PDF automaticamente
   - Atualizar o `index.md`
   - Publicar no GitHub Pages

## 🔧 Configuração Inicial (Já Feita)

- [x] GitHub Pages configurado para usar **GitHub Actions** como source
- [x] Workflow consolidado (update + deploy em uma única execução)
- [x] Script Python com detecção inteligente de múltiplos cargos na mesma empresa
- [x] Tema Jekyll dark-poole-master

## 📝 Features do Script Python

- ✅ Preserva **toda** a informação do PDF
- ✅ Detecta automaticamente múltiplos cargos na mesma empresa
- ✅ Formata corretamente skills, experiência, educação e certificados
- ✅ Gera links clicáveis (LinkedIn, GitHub)
- ✅ Mantém formatação de bullet points
- ✅ Rastreia última versão processada (evita reprocessamento)

## 🌐 Acesso ao Site

Depois do deploy, seu portfólio estará disponível em:
- **URL Principal**: `https://guilhermeldcosta.github.io/portfolio-v2/`
- (ou seu domínio customizado se configurado)

## 🐛 Troubleshooting

### Workflow não está rodando?
- Verifique se o push foi para a branch `master`
- Confirme que o arquivo está em `resumes/**`
- Cheque se GitHub Actions está habilitado em Settings → Actions

### Deploy falhou?
- Vá na aba Actions e veja os logs do workflow
- Confirme que GitHub Pages está configurado para "GitHub Actions" (não "Deploy from a branch")

### PDF não foi processado?
- Verifique se o número da revisão (rev-X) é maior que o valor em `last_processed.txt`
- Confirme que o nome segue o padrão: `resume-guilherme-costa-en-rev-X.pdf`
