try {
  window.addEventListener('load', corners_go, false);
} catch(e) {
  window.attachEvent('onload', corners_go);
}

function corners_go() {
  inittop();
  initbot();
  initall();
}

function inittop() {
  var settings = {
    tl: { radius: 10 },
    tr: { radius: 10 },
    bl: { radius: 00 },
    br: { radius: 00 },
    antiAlias: true
  }

  curvyCorners(settings, '.roundtop');
}


function initbot() {
  var settings = {
    tl: { radius: 00 },
    tr: { radius: 00 },
    bl: { radius: 10 },
    br: { radius: 10 },
    antiAlias: true
  }

  curvyCorners(settings, '.roundbottom');
}


function initall() {
  var settings = {
    tl: { radius: 10 },
    tr: { radius: 10 },
    bl: { radius: 10 },
    br: { radius: 10 },
    antiAlias: true
  }

  curvyCorners(settings, '.roundall');
}
