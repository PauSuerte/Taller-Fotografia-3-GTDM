import cv2
import numpy as np
import os
import glob

def load_images(images):
    ims= []
    for i in images:
        image = cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB)
        ims.append(image)

    return ims

def align(im1, im2):
    # IMAGENES EN ESCALA DE GRISES
    im1_gray = cv2.cvtColor(im1,cv2.COLOR_RGB2GRAY)
    im2_gray = cv2.cvtColor(im2,cv2.COLOR_RGB2GRAY)

    # TAMAÑO DE LA PRIMERA IMAGEN
    sz = im1.shape

    warp_mode = cv2.MOTION_TRANSLATION
    # LAS SIGUIENTES IMPLEMENTACIONES TARDAN MUCHO TIEMPO Y NO MEJORAN EN EXCESO LA IMAGEN FINAL
    # warp_mode = cv2.MOTION_HOMOGRAPHY
    # warp_mode = cv2.MOTION_AFFINE

    # DEFINE MATRICES 2x3 o 3x3 E INICIALIZA LA MATRIZ IDENTIDAD
    if warp_mode == cv2.MOTION_HOMOGRAPHY :
        warp_matrix = np.eye(3, 3, dtype=np.float32)
    else :
        warp_matrix = np.eye(2, 3, dtype=np.float32)

    # NUMERO DE INTERACCIONES
    interacciones = 5000;

    # ESPECIFICA EL LIMITE DEL INCREMENTO ENTRE DOS INTERACCIONES
    termination_eps = 1e-10;
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, interacciones,  termination_eps)
    (cc, warp_matrix) = cv2.findTransformECC (im1_gray, im2_gray, warp_matrix, warp_mode, criteria)

    if warp_mode == cv2.MOTION_HOMOGRAPHY : 
        im2_aligned = cv2.warpPerspective(im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    else :
        im2_aligned = cv2.warpAffine(im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    return im2_aligned

def align_images(images):
    im0 = images[len(images)//2]
    aligned_image_list = []
    cont = 0
    for im in images:
        cont += 1
        print(f'   ALINEANDO imagen {cont}')
        aligned_image_list.append(align(im0, im))
    return aligned_image_list


def doLap(image):

    # VALORES A RETOCAR (IDEAL: los dos valores similares e impares)
    kernel_size = 5         # VENTANA LAPLACIANA (PASO ALTO)
    blur_size   = 5         # BLUR GAUSSIANO (PASO BAJO)

    blurred = cv2.GaussianBlur(image, (blur_size,blur_size), 0)
    return cv2.Laplacian(blurred, cv2.CV_64F, ksize=kernel_size)


def focus_stack(unimages):
    images = align_images(unimages)

    print('   REALIZANDO EL FOCUS-STACKING')
    laps = []
    for i in range(len(images)):
        laps.append(doLap(cv2.cvtColor(images[i],cv2.COLOR_BGR2GRAY)))

    laps = np.asarray(laps)

    output = np.zeros(shape=images[0].shape, dtype=images[0].dtype)

    for y in range(0,images[0].shape[0]):
        for x in range(0, images[0].shape[1]):
            yxlaps = abs(laps[:, y, x])
            index = (np.where(yxlaps == max(yxlaps)))[0][0]
            output[y,x] = images[index][y,x]
    return output

def main(nameSalida,imagenes,dirname):
    
    ims = load_images(imagenes)

    im = focus_stack(ims)

    # GUARDAR IMAGEN - [se guarda como png en el directorio especificado]
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.path.join(dirname , nameSalida), im)  
        
    print('FINALIZADO')
    
    return True
