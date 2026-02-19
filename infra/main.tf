resource "local_file" "demo" {
  content  = "OpenSpec + OpenTofu test"
  filename = "infra/demo.txt"
}
