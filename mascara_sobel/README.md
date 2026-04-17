# Filtro de Bordas Sobel - Projeto Python + OpenCV

## Descrição do Projeto

Este projeto implementa a detecção de bordas usando o filtro de Sobel com Python e OpenCV. O objetivo é converter imagens em representações de contorno que destacam transições abruptas de intensidade e bordas de objetos.

Ele facilita a experimentação com diferentes configurações de qualidade, incluindo pré-processamento, pós-processamento e visualização dos resultados.

## O que este projeto faz

- processa arquivos de imagem únicos ou diretórios inteiros (`dataset`)
- converte imagens para escala de cinza
- aplica o filtro Sobel com gradientes horizontais e verticais
- normaliza bordas para uma saída visualmente consistente
- permite filtros avançados para melhorar qualidade e reduzir ruído
- salva imagens resultantes em disco
- exibe o resultado na tela se solicitado

## Principais recursos

- `Python + OpenCV` para processamento eficiente
- Suporte a processamento em lote de imagens
- Ajustes de qualidade:
  - tamanho do kernel Sobel (`ksize`)
  - blur gaussiano de pré-processamento
  - equalização de histograma
  - filtro bilateral
  - operações morfológicas
  - combinação com detecção de bordas Canny
- Visualização dinâmica das imagens com `--show`

## Estrutura do repositório

- `README.md` — documentação e instruções
- `requirements.txt` — dependências do projeto
- `sobel_edge_detection.py` — script principal de processamento
- `start.bat` — atalho para executar o modo HARD
- `dataset/` — pasta de referência para imagens de entrada

## Requisitos

- Python 3.8 ou superior
- OpenCV
- NumPy

Instalação das dependências:

```bash
pip install -r requirements.txt
```

## Como usar

### Processar uma imagem única

```bash
python sobel_edge_detection.py caminho/para/imagem.jpg --output resultado.png --threshold 100 --show
```

### Processar um diretório de imagens

```bash
python sobel_edge_detection.py dataset --output dataset_sobel --threshold 100 --show
```

### Exemplo de modo HARD

```bash
python sobel_edge_detection.py dataset --output dataset_sobel --ksize 5 --blur 5 --blur-sigma 1.0 --equalize --bilateral --morph gradient --morph-ksize 5 --canny --canny-th1 50 --canny-th2 150 --threshold 100 --show
```

Esse comando aplica:
- `GaussianBlur` para reduzir ruído antes do Sobel
- equalização de histograma para melhorar contraste
- filtro bilateral para suavização preservando bordas
- Sobel com kernel maior (`ksize=5`)
- combinação com Canny para reforçar bordas
- operação morfológica `gradient` para refinar contornos

## Parâmetros disponíveis

- `input_path`: arquivo de imagem ou diretório de imagens
- `-o, --output`: caminho do arquivo ou diretório de saída
- `-t, --threshold`: limiar para bordas fortes
- `--ksize`: tamanho do kernel Sobel (`1`, `3`, `5`, `7`)
- `--blur`: tamanho do kernel `GaussianBlur`
- `--blur-sigma`: sigma do `GaussianBlur`
- `--equalize`: equaliza o histograma do grayscale
- `--bilateral`: aplica filtro bilateral
- `--morph`: operação morfológica pós-Sobel (`none`, `open`, `close`, `gradient`, `tophat`, `blackhat`)
- `--morph-ksize`: tamanho do kernel morfológico
- `--canny`: combina Sobel com Canny
- `--canny-th1` / `--canny-th2`: thresholds do Canny
- `--show`: exibe a imagem original e a imagem filtrada
  - para diretórios, cada imagem é exibida em sequência
  - pressione qualquer tecla para avançar ou `q` para interromper

## Como funciona o script

1. lê a imagem ou diretório de imagens
2. converte para escala de cinza
3. aplica pré-processamento opcional (`blur`, `equalize`, `bilateral`)
4. calcula gradientes Sobel e magnitude de borda
5. aplica pós-processamento opcional (`threshold`, morfologia, Canny)
6. salva o resultado
7. exibe a imagem se `--show` estiver ativado

## Como usar o `start.bat`

Execute `start.bat` para abrir automaticamente o modo HARD e processar o diretório `dataset` com parâmetros avançados.

## Melhores práticas e melhorias futuras

- comparar Sobel com outros filtros de detecção de bordas (Prewitt, Roberts, Canny)
- adicionar interface gráfica ou demonstração web
- incluir processamento de vídeo em tempo real
- gerar relatórios de métricas e qualidade

## Referências

- Sobel Edge Detection
- Processamento de Imagem
- Visão Computacional
