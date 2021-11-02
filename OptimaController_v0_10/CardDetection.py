import cv2
# import numpy as np
import os


class CardDetection:
    FILES_DIRECTORY = 'images/cards/sample/'

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def find_countours_of_cards(self, img):
        # гауссово размытие, для того, чтобы было легче найти контуры карт.
        blurred = cv2.GaussianBlur(img, (3, 3), 0)

        # любое значение пикселя, превышающее 215, устанавливается равным 255,
        # а любое значение, которое меньше 215, устанавливается равным нулю
        T, thresh_img = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)

        (_, cnts, _) = cv2.findContours(thresh_img, cv2.RETR_LIST,
                                        cv2.CHAIN_APPROX_SIMPLE)
        # print(type(cnts))
        return cnts

    def find_coordinates_of_cards(self, cnts, img, edge=15):

        cards_coords = {}
        for i in range(0, len(cnts)):
            # находим координаты и размер найденных контуров
            x, y, w, h = cv2.boundingRect(cnts[i])
            if w > 80 and h > 120:
                try:
                    img_crop = img[y - edge:y + h + edge,
                               x - edge:x + w + edge]
                    cards_name = self.find_features(img_crop)
                    cards_coords[cards_name] = (x - edge, y - edge,
                                                x + w + edge, y + h + edge)
                except:
                    pass
        return cards_coords

    def find_features(self, img1):
        correct_matches_dict = {}
        # print(os.listdir(FILES_DIRECTORY))
        for image in os.listdir(self.FILES_DIRECTORY):
            img2 = cv2.imread(self.FILES_DIRECTORY + image, 0)
            # обнаружение ключевых точек
            orb = cv2.ORB_create()
            kp1, des1 = orb.detectAndCompute(img1, None)
            kp2, des2 = orb.detectAndCompute(img2, None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            correct_matches = []
            for m, n in matches:
                # if m.distance < 0.75*n.distance:
                if m.distance < 0.5 * n.distance:
                    correct_matches.append([m])
                    correct_matches_dict[image.split('.')[0]] = len(correct_matches)
        correct_matches_dict = dict(sorted(correct_matches_dict.items(),
                                           key=lambda item: item[1], reverse=True))
        print(list(correct_matches_dict.keys()))
        # возвращаем список ключевых точек
        return list(correct_matches_dict.keys())[0]


    def draw_rectangle_aroudn_cards(self, cards_coords, image):
        for key, value in cards_coords.items():
            rec = cv2.rectangle(image, (value[0], value[1]), (value[2], value[3]),
                                (255, 255, 0), 2)
            cv2.putText(rec, key, (value[0], value[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)
            # print(key)
        cv2.imshow('Press "Esc" button, for exit', image)
        # cv2.waitKey(0)
        try:
            return key
        except:
            pass


def main(img, cd):

    main_img = img
    gray_img = cv2.cvtColor(main_img, cv2.COLOR_BGR2GRAY)

    cnts = cd.find_countours_of_cards(gray_img)

    card_location = cd.find_coordinates_of_cards(cnts, gray_img)
    cd.draw_rectangle_aroudn_cards(card_location, main_img)


if __name__ == '__main__':

    cd = CardDetection()

    cap = cv2.VideoCapture(0)

    while True:
        try:
            flag, img = cap.read()

            main(img, cd)
        except:
            cap.release()
            raise
        ch = cv2.waitKey(5)
        if ch == 27:
            break
