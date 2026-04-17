import argparse
import os
from typing import List, Optional

import cv2
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(
        description='Aplicar filtro de borda Sobel em uma imagem ou diretório de imagens usando Python e OpenCV.'
    )
    parser.add_argument('input_path', help='Caminho da imagem de entrada ou diretório contendo imagens')
    parser.add_argument(
        '-o', '--output', default=None,
        help='Caminho do arquivo de saída ou diretório de saída. Se não informado, usa sobel_output.png ou sobel_output/.'
    )
    parser.add_argument(
        '-t', '--threshold', type=int, default=0,
        help='Limiar opcional para destacar bordas mais fortes (0 = sem limiar)'
    )
    parser.add_argument(
        '--ksize', type=int, choices=[1, 3, 5, 7], default=3,
        help='Tamanho do kernel Sobel (valores ímpares, maiores suavizam mais).'
    )
    parser.add_argument(
        '--blur', type=int, default=0,
        help='Tamanho do kernel GaussianBlur para pré-processamento. 0 desativa o blur.'
    )
    parser.add_argument(
        '--blur-sigma', type=float, default=1.0,
        help='Sigma para GaussianBlur (usado se --blur for > 0).'
    )
    parser.add_argument(
        '--equalize', action='store_true',
        help='Aplicar equalização de histograma ao grayscale antes de Sobel.'
    )
    parser.add_argument(
        '--bilateral', action='store_true',
        help='Aplicar filtro bilateral ao grayscale antes de Sobel para suavizar sem perder bordas.'
    )
    parser.add_argument(
        '--morph', choices=['none', 'open', 'close', 'gradient', 'tophat', 'blackhat'],
        default='none',
        help='Operação morfológica opcional aplicada após Sobel.'
    )
    parser.add_argument(
        '--morph-ksize', type=int, default=3,
        help='Tamanho do kernel morfológico (valor ímpar).' 
    )
    parser.add_argument(
        '--canny', action='store_true',
        help='Combinar resultado Sobel com Canny para bordas mais nítidas.'
    )
    parser.add_argument(
        '--canny-th1', type=int, default=100,
        help='Threshold 1 para Canny (se --canny estiver ativado).'
    )
    parser.add_argument(
        '--canny-th2', type=int, default=200,
        help='Threshold 2 para Canny (se --canny estiver ativado).'
    )
    parser.add_argument(
        '--show', action='store_true',
        help='Exibir a imagem original e a imagem filtrada em janelas. Para diretórios, mostra as imagens em sequência.'
    )
    return parser.parse_args()


def is_image_file(path: str) -> bool:
    supported_ext = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp'}
    _, ext = os.path.splitext(path.lower())
    return ext in supported_ext


def list_images(input_path: str) -> List[str]:
    if os.path.isdir(input_path):
        return sorted(
            os.path.join(input_path, f)
            for f in os.listdir(input_path)
            if is_image_file(f)
        )
    return [input_path]


def get_output_path(input_path: str, output_arg: Optional[str], is_dir: bool) -> str:
    if is_dir:
        output_dir = output_arg or 'sobel_output'
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    if output_arg is None:
        return 'sobel_output.png'

    if os.path.isdir(output_arg):
        base_name = os.path.basename(input_path)
        return os.path.join(output_arg, base_name)

    return output_arg


def preprocess_image(gray_image: np.ndarray, blur: int, blur_sigma: float, equalize: bool, bilateral: bool) -> np.ndarray:
    processed = gray_image.copy()
    if blur > 0:
        blur_size = blur if blur % 2 == 1 else blur + 1
        processed = cv2.GaussianBlur(processed, (blur_size, blur_size), blur_sigma)
    if equalize:
        processed = cv2.equalizeHist(processed)
    if bilateral:
        processed = cv2.bilateralFilter(processed, 9, 75, 75)
    return processed


def apply_morphology(image: np.ndarray, operation: str, ksize: int) -> np.ndarray:
    if operation == 'none':
        return image
    morph_size = ksize if ksize > 0 and ksize % 2 == 1 else max(3, ksize + 1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (morph_size, morph_size))
    ops = {
        'open': cv2.MORPH_OPEN,
        'close': cv2.MORPH_CLOSE,
        'gradient': cv2.MORPH_GRADIENT,
        'tophat': cv2.MORPH_TOPHAT,
        'blackhat': cv2.MORPH_BLACKHAT,
    }
    return cv2.morphologyEx(image, ops[operation], kernel)


def compute_sobel(gray_image: np.ndarray, ksize: int) -> np.ndarray:
    gx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=ksize)
    gy = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=ksize)
    magnitude = np.sqrt(np.square(gx) + np.square(gy))
    max_val = np.max(magnitude)
    if max_val > 0:
        magnitude = np.uint8(np.clip((magnitude / max_val) * 255.0, 0, 255))
    else:
        magnitude = np.zeros_like(gray_image, dtype=np.uint8)
    return magnitude


def combine_with_canny(sobel_image: np.ndarray, gray_image: np.ndarray, th1: int, th2: int) -> np.ndarray:
    edges = cv2.Canny(gray_image, th1, th2)
    return np.maximum(sobel_image, edges)


def apply_threshold(image: np.ndarray, threshold: int) -> np.ndarray:
    if threshold <= 0:
        return image
    _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return binary


def main():
    args = parse_args()
    input_path = args.input_path

    if not os.path.exists(input_path):
        raise FileNotFoundError(f'Caminho não encontrado: {input_path}')

    image_paths = list_images(input_path)
    if len(image_paths) == 0:
        raise FileNotFoundError(f'Nenhuma imagem válida encontrada em: {input_path}')

    if os.path.isdir(input_path):
        output_dir = get_output_path(input_path, args.output, is_dir=True)
        print(f'Processando diretório: {input_path}')
        print(f'Salvando resultados em: {output_dir}')

        for image_path in image_paths:
            image = cv2.imread(image_path)
            if image is None:
                print(f'Aviso: falha ao carregar {image_path}, pulando.')
                continue

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = preprocess_image(gray, args.blur, args.blur_sigma, args.equalize, args.bilateral)
            sobel = compute_sobel(gray, args.ksize)
            if args.canny:
                sobel = combine_with_canny(sobel, gray, args.canny_th1, args.canny_th2)
            sobel = apply_morphology(sobel, args.morph, args.morph_ksize)
            output_image = apply_threshold(sobel, args.threshold)

            output_path = os.path.join(output_dir, os.path.basename(image_path))
            cv2.imwrite(output_path, output_image)
            print(f'Imagem salva: {output_path}')

            if args.show:
                cv2.imshow('Original', image)
                cv2.imshow('Sobel', output_image)
                print('Pressione qualquer tecla para continuar ou q para sair...')
                key = cv2.waitKey(0) & 0xFF
                cv2.destroyAllWindows()
                if key == ord('q'):
                    print('Exibição interrompida pelo usuário.')
                    break

        print(f'Processamento concluído. Total de imagens processadas: {len(image_paths)}')
        return

    output_path = get_output_path(input_path, args.output, is_dir=False)
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError('Falha ao carregar a imagem. Verifique o caminho e o formato.')

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = preprocess_image(gray, args.blur, args.blur_sigma, args.equalize, args.bilateral)
    sobel = compute_sobel(gray, args.ksize)
    if args.canny:
        sobel = combine_with_canny(sobel, gray, args.canny_th1, args.canny_th2)
    sobel = apply_morphology(sobel, args.morph, args.morph_ksize)
    output = apply_threshold(sobel, args.threshold)

    cv2.imwrite(output_path, output)
    print(f'Imagem Sobel salva em: {output_path}')

    if args.show:
        cv2.imshow('Original', image)
        cv2.imshow('Sobel', output)
        print('Pressione qualquer tecla na janela para sair...')
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
