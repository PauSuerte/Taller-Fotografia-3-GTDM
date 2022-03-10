import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# https://datahacker.rs/005-how-to-create-a-panorama-image-using-opencv-with-python/

# Funcion para juntar imagenes
def warpImages(img1, img2, H):

    rows1, cols1 = img1.shape[:2]
    rows2, cols2 = img2.shape[:2]

    list_of_points_1 = np.float32([[0,0], [0, rows1],[cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2)
    temp_points = np.float32([[0,0], [0,rows2], [cols2,rows2], [cols2,0]]).reshape(-1,1,2)

    # When we have established a homography we need to warp perspective
    # Change field of view
    list_of_points_2 = cv2.perspectiveTransform(temp_points, H)

    list_of_points = np.concatenate((list_of_points_1,list_of_points_2), axis=0)

    [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)
    
    translation_dist = [-x_min,-y_min]
    
    H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

    output_img = cv2.warpPerspective(img2, H_translation.dot(H), (x_max-x_min, y_max-y_min))
    output_img[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]:cols1+translation_dist[0]] = img1

    return output_img

def pan(im1, im2):
    # Crear orbes para detectar puntos de interes de las imagenes
    orb = cv2.ORB_create(nfeatures=2000)

    # Buscar puntos de interes en las imagenes
    keypoints1, descriptors1 = orb.detectAndCompute(im1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2, None)

    # Se crea un objeto BFMatcher, el cual se ocupa de juntar los puntos de interes de las dos imagenes
    bf = cv2.BFMatcher_create(cv2.NORM_HAMMING)

    # Se buscan los puntos de interes en comun a traves de los descriptors, los cuales indican donde estan los keypoints
    # K=2, buscara en los 2 vecinos mas proximos al punto una coincidencia
    matches = bf.knnMatch(descriptors1, descriptors2,k=2)

    # De la siguiente forma se obtienen los mejores matches
    good = []
    for m, n in matches:
        if m.distance < 0.6 * n.distance:
            good.append(m)

    # Set minimum match condition
    MIN_MATCH_COUNT = 5

    if len(good) > MIN_MATCH_COUNT:
        # Convert keypoints to an argument for findHomography
        src_pts = np.float32([ keypoints1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        dst_pts = np.float32([ keypoints2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

        # Establish a homography
        M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        
        result = warpImages(im2, im1, M)

        # cv2.imshow("resultado",result)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        return result

def crop(paneoFinal):
    gray = cv2.cvtColor(paneoFinal,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    countours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt = countours[0]
    x,y,w,h = cv2.boundingRect(cnt)

    crop = paneoFinal[y:y+h,x:x+w]
    return crop

def progPaneo(nomSalida,cantidad,imagenes,pathRes):
    paneos = {}

    for j in range (cantidad-1):
        paneos[str(j)] = pan(imagenes[str(j)],imagenes[str(j+1)])

    if cantidad>2:
        result = pan(paneos["0"],paneos["1"])
        cv2.imwrite(os.path.join(pathRes , nomSalida), result)

        # Prueba crop
        # resultCROP = crop(result)
        # cv2.imwrite('CROPEADO'+nomSalida, resultCROP)
        return True
    
    else:
        cv2.imwrite(os.path.join(pathRes , nomSalida), paneos["0"])
        
        # Prueba crop
        # resultCROP = crop(paneos["0"])
        # cv2.imwrite('CROPEADO'+nomSalida, resultCROP)
        return True