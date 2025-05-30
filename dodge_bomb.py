import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {#辞書
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True#横、縦方向用の変数
    #横方向判定
    if rct.left < 0 or WIDTH < rct.right:#画面外だったら
        yoko = False
    #縦方向判定
    if rct.top < 0 or HEIGHT < rct.bottom:#画面外だったら
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:#Game over画面
    
    bg_img = pg.Surface((WIDTH, HEIGHT))#黒背景
    pg.draw.rect(bg_img, (0, 0, 0),(0, 0, WIDTH, HEIGHT))
    bg_img.set_alpha(200)
    screen.blit(bg_img, [0, 0])
    #左こうかとん
    kk_img2 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct2 = kk_img2.get_rect()
    kk_rct2.center = 360, 320
    screen.blit(kk_img2, kk_rct2)
    #右こうかとん
    kk_img3 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct3 = kk_img3.get_rect()
    kk_rct3.center = 740, 320
    screen.blit(kk_img3, kk_rct3)
    #Game over文字
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game over",True, (255, 255, 255))
    screen.blit(txt, [400, 300])


#def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:#爆弾の拡大


#def calc_orientation(org: pg.Rect, dst: pg.Rect,current_xy: tuple[float, float]) -> tuple[float, float]:#追従型爆弾


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    #こうかとん初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    #爆弾初期化
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx, vy = +5, +5


    #拡大
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)


    # 加速度リスト
    bb_accs = [a for a in range(1, 11)]
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    vx,vy = (+5, +5)  
    

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            #print("Game over")
            gameover(screen)
            pg.display.update()
            time.sleep(5)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]#左右方向
                sum_mv[1] += mv[1]#上下方向

        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):#画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])#画面内に戻す
        screen.blit(kk_img, kk_rct)

        #爆弾の画像と速度の更新
        bb_img = bb_imgs[min(tmr//500, 9)]
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]


        bb_rct.move_ip(avx, avy) # 加速して移動

        bb_rct.move_ip(vx,vy)#爆弾の移動
        yoko ,tate = check_bound(bb_rct)
        if not yoko:#左右どちらかにはみ出ていたら
            vx *= -1
        if not tate:#上下どちらかにはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)#爆弾の描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()