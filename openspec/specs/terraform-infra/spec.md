### Requirement: Terraform/OpenTofu initialization
The system SHALL initialize Terraform/OpenTofu using the local provider with version >= 1.6.0.

#### Scenario: Successful initialization
- **WHEN** running `tofu init` in the infra directory
- **THEN** Terraform/OpenTofu downloads the local provider version ~> 2.3
- **AND** the local backend is configured with state file at `terraform.tfstate`

### Requirement: Local file resource management
The system SHALL manage local file resources through Terraform/OpenTofu configuration.

#### Scenario: Create demo file
- **WHEN** applying Terraform configuration
- **THEN** a file named `demo.txt` is created in the `infra/` directory
- **AND** the file content contains "OpenSpec + OpenTofu test"

### Requirement: Variable configuration
The system SHALL support variable definition with default values in Terraform.

#### Scenario: Use default variable
- **WHEN** running Terraform operations without explicit variable values
- **THEN** the `example_var` variable defaults to "test"
- **AND** the variable type is validated as string

### Requirement: CI/CD integration with GitHub Actions
The system SHALL integrate Terraform/OpenTofu workflows with GitHub Actions on pull requests to main branch.

#### Scenario: CI workflow execution
- **WHEN** a pull request is created or updated targeting main branch
- **THEN** GitHub Actions workflow "Terraform + OpenSpec CI" is triggered
- **AND** OpenTofu v1.10.7 is installed
- **AND** `tofu init` is executed successfully
- **AND** `tofu plan` is executed to validate configuration

### Requirement: State management
The system SHALL maintain Terraform state using local backend.

#### Scenario: State file creation
- **WHEN** Terraform is initialized
- **THEN** the state file is created at `infra/terraform.tfstate`
- **AND** state is stored locally on the filesystem

### Requirement: Provider constraints
The system SHALL enforce provider version constraints for consistency.

#### Scenario: Provider version validation
- **WHEN** running `tofu init`
- **THEN** the local provider version ~> 2.3 is validated
- **AND** Terraform/OpenTofu version >= 1.6.0 is verified