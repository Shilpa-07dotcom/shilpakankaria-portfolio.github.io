import sys, numpy as np
from PIL import Image
from scipy import ndimage

def cut(inp, outp, white=236, min_frac=0.004, feather=1.2):
    im = Image.open(inp).convert("RGB")
    a = np.array(im).astype(np.int16)
    R,G,B = a[...,0],a[...,1],a[...,2]
    mx=a.max(2); mn=a.min(2)
    nearwhite=(R>white)&(G>white)&(B>white)&((mx-mn)<14)
    fg=~nearwhite
    fg=ndimage.binary_opening(fg, structure=np.ones((3,3)), iterations=1)
    fg=ndimage.binary_fill_holes(fg)
    lbl,n=ndimage.label(fg)
    if n>0:
        sizes=ndimage.sum(np.ones_like(lbl),lbl,range(1,n+1))
        thr=fg.size*min_frac
        keep=np.zeros(fg.shape,bool)
        for i,s in enumerate(sizes,1):
            if s>=thr: keep|=(lbl==i)
        fg=ndimage.binary_fill_holes(keep)
    alpha=ndimage.gaussian_filter((fg*255).astype(np.float32),feather)
    out=np.dstack([np.array(im),alpha.astype(np.uint8)])
    # autocrop to content
    ys,xs=np.where(alpha>8)
    if len(xs):
        pad=12
        x0,x1=max(xs.min()-pad,0),min(xs.max()+pad,out.shape[1])
        y0,y1=max(ys.min()-pad,0),min(ys.max()+pad,out.shape[0])
        out=out[y0:y1,x0:x1]
    Image.fromarray(out,"RGBA").save(outp)
    print(f"OK {outp} {out.shape[1]}x{out.shape[0]} fg={fg.mean()*100:.1f}%")

def preview(cutpng, bg, outp):
    fg=Image.open(cutpng).convert("RGBA")
    canvas=Image.new("RGBA",(fg.width+160,fg.height+160),bg)
    canvas.alpha_composite(fg,(80,80))
    canvas.convert("RGB").save(outp,quality=90)
    print("preview",outp)

if __name__=="__main__":
    cut(sys.argv[1],sys.argv[2])
    if len(sys.argv)>3:
        preview(sys.argv[2],(236,235,247,255),sys.argv[3])
