Projeto simples para simular falhas controladas para testes de resiliencia.
 Inclui API em fastAPI e interface web em HTML, CSS e JS.

 Como executar
Acesse a pasta backend:
cd backend
Execute o servidor:
uvicorn main:app --reload
Abra no navegador:
http://127.0.0.1:8000

Agora basta monitorar no seu gestor de recursos a funcionalidade.

por docker:
 docker run --rm -p 8000:8000 rickdevops/chaos-api:v1
