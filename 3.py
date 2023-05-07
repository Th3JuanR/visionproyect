#Exportamos las librerias las cuales vamos a utilizar
import cv2
import numpy as np 
import math
# En esta funcion para definir los colores el cual vamos a utilizar 
# Utilizamso los colores en formato HSV = (Matiz(H),Saturacion(S),Brillo(V))
def figColor(imagenHSV):
    # Rojo 
    rojoBajo1 = np.array([0,100,20],np.uint8) # Utilizamos la funcion np.array para definir lo rangos del color rojo en el espacio (hsv)
    rojoAlto1 = np.array([10,255,255],np.uint8)
    rojoBajo2 = np.array([175,100,20],np.uint8)
    rojoAlto2 = np.array([180,255,255],np.uint8)
    
    # Amarillo
    amarilloBajo = np.array([20,100,20],np.uint8)
    amarilloAlto = np.array([32,255,255],np.uint8)
    
    # Verde
    verdeBajo = np.array([36,100,20],np.uint8)
    VerdeAlto = np.array([70,255,255],np.uint8)
    
    # Buscamos los colores en la imagen, según los límites 
    maskRojo1 = cv2.inRange(imagenHSV, rojoBajo1, rojoAlto1)
    maskRojo2 = cv2.inRange(imagenHSV, rojoBajo2, rojoAlto2)
    maskRojo = cv2.add(maskRojo1, maskRojo2)
    maskAmarillo = cv2.inRange(imagenHSV, amarilloBajo, amarilloAlto)
    maskVerde = cv2.inRange(imagenHSV, verdeBajo, VerdeAlto)
    
    #Utilizamos findCountours para encontrar los los contornes de la imagen
    cntsRojo = cv2.findContours(maskRojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cntsAmarillo = cv2.findContours(maskAmarillo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    cntsVerde = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    
    color = ''
    
    if len(cntsRojo) > 0:
        color = 'Rojo'
    elif len(cntsAmarillo) > 0:
        color = 'Amarillo'
    elif len(cntsVerde) > 0:
        color = 'Verde'
    
    return color

"""Listo ahora pasamos a que el codigo sea capaz de deteminar que figura es"""
def figShape(contorno, width=None, height=None):
    ''' Esta función toma 3 parametros en este caso es contorno, ancho y alto '''
    epsilon = 0.1*cv2.arcLength(contorno, True) # esta parte es para calcular el perimetro del contorno
    approx = cv2.approxPolyDP(contorno, epsilon, True) # aqui aproximamos el contorno de un poligo y la funcion epsilon es un parametro que especifica la precision de la aproximacion

    vertices = len(approx)
    
    if vertices < 3:
        return 'No es una figura'
    elif vertices == 3:
        return 'Triángulo'
    elif vertices == 4:
        if cv2.isContourConvex(approx): #La funcion que se utiliza aqui es para saber si la figura es convexa o no
            if width and height:
                aspect_ratio = float(width)/height
                if 0.95 <= aspect_ratio <= 1.05:
                    return 'Cuadrado'
                else:
                    return 'Rectángulo'
            else:
                return 'Cuadrado'
        else:
            return 'Rectángulo'
    elif vertices == 5:
        return 'Pentágono'
    elif vertices == 6:
        return 'Hexágono'
    else:
        perimeter = cv2.arcLength(contorno, True) 
        if vertices >= 10 and abs(area - math.pi * (perimeter / (2 * math.pi)) ** 2) < 100:
            return 'Círculo'
        else:
            return 'Figura con demasiados lados'

   
    #if len(approx) == 3:
        #shape = 'Triangulo'
        
    #elif len(approx) == 4:
        #aspect_ratio = float(width) / height
        
        #if aspect_ratio == 1:
            #namefig = 'Cuadrado'
        #else:
            #namefig = 'Rectangulo'
    #elif len(approx) == 5:
        #namefig = 'Pentagono'
    #elif len(approx) == 6:
       # namefig = 'Hexagono'
    #elif len(approx) > 10:
     #   namefig = 'Circulo'
    
    #return namefig

#PARTE DEL TAMAÑO 

def classify_shape_and_size(area, equi_diameter_units):
    if area > 0:
        if equi_diameter_units >= 5:
            size = "Grande"
        elif equi_diameter_units >= 4:
            size = "Mediano"
        else:
            size = "Pequeño"
    else:
        size = ""
    
    if num_vertices == 3:
        shape = "Triángulo"
    elif num_vertices == 4:
        shape = "Cuadrado o Rectángulo"
    else:
        shape = "Círculo"
        
    return shape, size


# Esta es la dirección IP de la cámara y su puerto
url = 'http://192.168.1.18:4747/video'

# Aquí se elige la cámara que se va a utilizar, en este caso la de la dirección IP mencionada anteriormente.
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()

    if ret == True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 10,150)
        canny = cv2.dilate(canny,None,iterations=1)
        canny = cv2.erode(canny,None,iterations=1)
        cnts,_ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        imageHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
         #Filtro de suavizado
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        #Umbral
        ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        #Contornos de las imagenes
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #Calibracion de la imagen
        # Establecer la escala de la imagen
        pixel_to_unit = 1  # 1 píxel = 1 unidad (por ejemplo, cm)

        # Dibujar una línea de referencia de tamaño conocido
        reference_length_pixels = 100  # Longitud de la línea de referencia en píxeles
        reference_length_units = 10  # Longitud de la línea de referencia en unidades físicas (por ejemplo, cm)
        cv2.line(frame, (50, 50), (50 + reference_length_pixels, 50), (255, 0, 0), 2)
        
        
        # Calcular la relación entre píxeles y unidades físicas
        pixel_to_unit = reference_length_units / reference_length_pixels

        #Realizar contornos
        for contour in contours:
          area = cv2.contourArea(contour)
          perimeter = cv2.arcLength(contour, True)
          approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
          num_vertices = len(approx)

        #diametro
        if num_vertices == 0:
            continue

        equi_diameter = np.sqrt(4 * area / np.pi)
        equi_diameter_units = equi_diameter * pixel_to_unit

        #forma y diametro
        shape, size = classify_shape_and_size(area, equi_diameter_units)
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
        cv2.putText(frame, "{} {}".format(shape, size), (contour[0][0][0], contour[0][0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            imAux = np.zeros(frame.shape[:2], dtype="uint8")
            imAux = cv2.drawContours(imAux, [c], -1, 255, -1)
            maskHSV = cv2.bitwise_and(imageHSV,imageHSV, mask=imAux)
            name = figShape(c,w,h)
            color = figColor(maskHSV)
            nameColor = name + ' ' + color

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite('foto.png',frame)
            print('Foto tomada con exito')
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()