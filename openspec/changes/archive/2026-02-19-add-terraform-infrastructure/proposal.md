## Why

O projeto chaos-api precisa de infraestrutura como código (IaC) para gerenciar de forma declarativa e versionável os recursos de nuvem necessários para a aplicação. O Terraform já está implementado na pasta `/infra`, mas precisa ser formalmente documentado e governado através do OpenSpec para garantir consistência, rastreabilidade e facilitar futuras mudanças.

## What Changes

- Documentação da infraestrutura Terraform existente através do OpenSpec
- Formalização dos recursos de nuvem definidos nos arquivos Terraform
- Estabelecimento de contratos claros para gerenciamento de infraestrutura
- Integração do workflow de IaC com o processo de mudanças do projeto

## Capabilities

### New Capabilities
- `terraform-infra`: Gerenciamento de infraestrutura como código usando Terraform, incluindo definição de recursos, providers, e configurações de provisionamento

### Modified Capabilities
- (Nenhuma - esta mudança documenta infraestrutura existente)

## Impact

- **Arquivos existentes**: `/infra/*.tf` (main.tf, provider.tf, variables.tf, versions.tf)
- **Workflow de CI/CD**: Integração com GitHub Actions já configurada em `.github/workflows/terraform.yml`
- **Documentação**: Criação de specs formais para governança de infraestrutura
- **Jenkinsfile**: Integração existente com pipeline de CI/CD