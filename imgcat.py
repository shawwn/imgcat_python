#!/usr/bin/env python3
import sys
import PIL.Image
from io import BytesIO
import os
import base64

def imgnorm(img):
  if img.dtype == 'float32':
    # Assumes range [-1 .. 1]
    img = img.copy()
    img *= 0.5
    img += 0.5
    img *= 255
    img = img.astype(np.uint8)
  return img

def image_to_bytes(img, format='PNG', **kwargs):
  b = BytesIO()
  img = numpy_to_image(img)
  img.save(b, format=format, **kwargs)
  return b.getvalue()

def osc():
  if os.environ.get('TERM').startswith('screen'):
    return "\033Ptmux;\033\033]"
  else:
    return "\033]"

def st():
  if os.environ.get('TERM').startswith('screen'):
    return "\a\033\\"
  else:
    return "\a"

def imgcat(img, name='test.png', width='auto', height='auto', preserve_aspect_ratio=True, *, file=sys.stdout):
  b = base64.b64encode(image_to_bytes(img)).decode('utf8')
  s = []
  s += [osc()]
  s += [('1337;File=')]
  s += ['name=%s;width=%s;height=%s;preserveAspectRatio=%s;' %
      (name, str(width), str(height), '1' if bool(int(preserve_aspect_ratio)) else '0')]
  s += ['size=%d' % len(b)]
  s += [';inline=%s' % '1']
  s += [':']
  s += ['%s' % b]
  s += ['%s' % st()]
  s = ''.join(s)
  file.write(s)

def numpy_to_image(img):
  if isinstance(img, PIL.Image.Image):
    return img
  return PIL.Image.fromarray(imgnorm(img))

if __name__ == '__main__':
  args = sys.argv[1:]
  for filename in args:
    img = PIL.Image.open(filename)
    imgcat(img,
        name=filename,
        width=os.environ.get('IMGW', 'auto'),
        height=os.environ.get('IMGH', 'auto'),
        preserve_aspect_ratio=os.environ.get('IMGR', '1'))
