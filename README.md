# Myssistant

Esse é o repositório para a disciplina de Reutilização de Software que incluí a parte pública e disponibilizável do código da Myssistant. Placeholders foram utilizados para emular as interações com a API.

Para executar o fluxo principal, faça uma requisição para /output.mp3?text="Sample_text'

Nessa versão do código, os áudios foram gerados previamente e não há geração de áudio em tempo real.

Para executar a aplicação em um container:

```
docker build -t myssistant-public . 
docker run -p 5000:5000 myssistant-public
```
