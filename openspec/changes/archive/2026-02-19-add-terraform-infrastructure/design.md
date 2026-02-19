## Context

O projeto chaos-api já possui infraestrutura Terraform implementada na pasta `/infra` com os arquivos principais (main.tf, provider.tf, variables.tf, versions.tf). A infraestrutura é executada através de workflows do GitHub Actions e integração com Jenkins. O objetivo desta mudança é formalizar a documentação e governança dessa infraestrutura existente através do OpenSpec.

### Current State

- Terraform já configurado com providers e recursos
- GitHub Actions workflow já existe em `.github/workflows/terraform.yml`
- Jenkinsfile integra o pipeline de CI/CD
- Infraestrutura operacional mas sem documentação formal de especificações

## Goals / Non-Goals

**Goals:**
- Documentar formalmente a infraestrutura Terraform existente
- Criar especificações claras para os recursos provisionados
- Estabelecer contrato entre infraestrutura e requisitos de negócio
- Facilitar futuras mudanças e revisões de infraestrutura

**Non-Goals:**
- Alterar a infraestrutura Terraform existente
- Migrar para provedores de nuvem diferentes
- Adicionar novos recursos Terraform além dos já existentes
- Modificar workflows de CI/CD atuais

## Decisions

### 1. Provider Selection
**Decision:** Utilizar provider(s) já definidos em provider.tf
**Rationale:** A infraestrutura já está funcional e em uso. Não há necessidade de alterar providers operacionais.
**Alternativas consideradas:**
- Alterar para novos providers (descartado - sem justificativa técnica)
- Migrar para multi-cloud (descartado - não é requisito atual)

### 2. State Management
**Decision:** Manter estratégia de state atual definida na infraestrutura
**Rationale:** Estado existente já está em produção. Mudanças poderiam causar indisponibilidade.
**Considerações:**
- Verificar configuração de backend em main.tf
- Garantir que state file está seguro e versionado

### 3. Documentation Approach
**Decision:** Documentar recursos existentes sem modificar configurações
**Rationale:** Esta é uma mudança de documentação/governança, não uma mudança técnica.
**Benefícios:**
- Zero risco para infraestrutura em produção
- Aumenta visibilidade e entendimento da arquitetura
- Prepara terreno para futuras mudanças informadas

### 4. CI/CD Integration
**Decision:** Manter workflows existentes (GitHub Actions + Jenkins)
**Rationale:** Pipelines já estão funcionando e testados.
**Documentação necessária:**
- Mapear cada workflow para recursos Terraform afetados
- Documentar triggers e automações existentes

## Risks / Trade-offs

### Risks
- [Risco] Documentação pode ficar desincronizada da infraestrutura real
  - **Mitigação:** Estabelecer processo de revisão quando infraestrutura mudar
- [Risco] Especificações podem não capturar todos os detalhes de implementação
  - **Mitigação:** Referenciar diretamente arquivos .tf para detalhes técnicos

### Trade-offs
- **Documentação vs. Agilidade:** Especificações formais adicionam passo extra para mudanças
  - **Aceitável:** Benefícios de governança superam custo adicional para infraestrutura crítica
- **Nível de detalhe:** Quanto detalhe incluir nas specs?
  - **Decisão:** Focar em contratos e requisitos, não em sintaxe Terraform

## Migration Plan

Esta mudança é puramente documentacional - não há migração técnica necessária.

**Passos:**
1. Criar spec formal para `terraform-infra`
2. Revisar e validar especificação contra infraestrutura real
3. Integrar especificação com processos de revisão de código
4. Atualizar documentação quando infraestrutura mudar no futuro

**Rollback:** Não aplicável - esta mudança não afeta infraestrutura em produção
