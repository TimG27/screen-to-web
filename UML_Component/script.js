var v1 = document.getElementById("");
var v2 = document.getElementById("");
var pname;
var s;

/*
function prevday() {
    let s = document.getElementById('Date').innerHTML;
    aas = s[0]+s[1]
    aas = parseInt(aas) - 1
    newd = aas + "/09/2022"
    document.getElementById('Date').innerHTML = newd;

    var rand = aas%4 + 1
    gennew(rand);
}

function nextday() {
    let s = document.getElementById('Date').innerHTML;
    aas = s[0]+s[1]
    aas = parseInt(aas) + 1
    newd = aas + "/09/2022"
    document.getElementById('Date').innerHTML = newd;

    var rand=aas%4 + 1
    gennew(rand);
}

function gennew (a) {

    var st = "col" + a
    var rm = document.getElementById(st)

    console.log(st);
    rm.remove();

    var ar = document.createElement('DIV');
    ar.setAttribute("class", "newscol")
    ar.setAttribute("id", st)
    
    var h34 = document.createElement('h3')
    h34.innerHTML = "Borem Mibsum"

    var img4 = document.createElement ('img')
    img4.setAttribute("src", "https://www.techsmith.com/blog/wp-content/uploads/2021/02/video-thumbnails-hero-1.png")
    img4.setAttribute("style", "height: 100px; width:200px")

    var p4 = document.createElement ('p')
    p4.innerHTML = ".murobal tse di mina tillom tnuresed aiciffo iuq apluc ni tnus ,tnediorp non tatadipuc taceacco tnis ruetpecxE .rutairap allun taiguf ue erolod mullic esse tilev etatpulov ni tiredneherper ni rolod eruri etua siuD .tauqesnoc odommoc ae xe piuqila tu isin sirobal ocmallu noitaticrexe durtson siuq ,mainev minim da mine tU .auqila angam erolod te erobal tu tnudidicni ropmet domsuie od des ,tile gnicsipida rutetcesnoc ,tema tis rolod muspi meroL"

    ar.appendChild(h34)
    ar.appendChild(img4)
    ar.appendChild(p4)

   var as = document.getElementById("anews");
    as.appendChild(ar);
}
*/

function genp() {

  var nam = prompt('Name of the user?')

  var prevmen = document.getElementById('menubar')

  var p = document.createElement('div')
  p.setAttribute("style","width: fit-content; height: min-content ;  padding: 5px; border-radius: 5px; background-color: skyblue; margin-left: 10px")
  p.id = nam

  p1 = document.createElement('p')
  p1.setAttribute("style", "justify-content: center; align-items:center;")
  p1.innerHTML = nam;

  p.addEventListener("mouseover",bl,false)
  p.addEventListener("mouseout",sk,false)


  function bl (){
    p.style = "background-color: green; width: fit-content; height: min-content ; align-items: center; padding: 5px; border-radius: 5px; margin-left: 10px"
  }

  function sk(){
    p.style = "background-color: skyblue; width: fit-content; height: min-content ; align-items: center; padding: 5px; border-radius: 5px; margin-left: 10px"
  }


  p.onclick = function() {sel(p.id);}

  var ca  = document.getElementById('cases')

  str = nam + "c"
  if (v1 == null) {
    v1 = document.createElement(str);
    v1.id = str;
    ca.appendChild(v1)
  }
  else if (v2 == null) {
    v2 = document.createElement(str);
    v2.id = str
    ca.appendChild(v2)
  }

  p.appendChild(p1)


  prevmen.appendChild(p)
}

function sel(x) {

  
  s = x

  console.log(s)

  var ca  = document.getElementById('cases')

  str = s + "c"

  if (v1.id == str) {
    v2.style.visibility = "hidden";
    v1.style.visibility = "visible"
    //ca.appendChild(v1);
  }
  else {
    v2.style.visibility = "visible";
    v1.style.visibility = "hidden";
    //ca.appendChild(v2)
  }

}

function gencs() {
  console.log (s)


  var c = prompt ('Enter the use case ');

  var t = document.createElement('div')
  t.style = "border: 1px solid black; display: flex; width:fit-content; padding: 5px; flex-direction: column; margin-left: 20px; margin-top: 20px;align-items: center; justify-content: center";

  var b0 = document.createElement ('h5')
  b0.innerHTML = c

  var br = document.createElement ('br')

  var b1 = document.createElement('input')
  b1.value = "Enter input here";

  var b15 = document.createElement('button')
  b15.setAttribute("type", "submit")
  b15.innerHTML = "Submit"

  
  var b2 = document.createElement ('input')
  b2.value = "Output here";

  t.appendChild(b0)
  t.appendChild(b1)
  t.appendChild(b15)
  t.appendChild(br)
  t.appendChild(b2)
  
  console.log(v1.id, v2.id)

  var str = s + "c"
  if (v1.id == str)
    v1.appendChild(t)
  else if (v2.id == str)
    v2.appendChild(t)

  //sel(s)
}

function initcanvas () {

  pname = document.getElementById('pname');
  console.log (pname.value)

  console.log (document.getElementById('uml').value)

  localStorage.setItem('pname', pname.value)

  //document.location.href = "canvas.html"
}

function loadcanvas() {

/*
  var m = document.createElement('img')
  m.src = document.getElementById('uml').src;

  console.log (m.src)

  m.width = "500px";

  var d = document.getElementById('diagram')

  d.appendChild(m)
  */


  var prevtitle = document.getElementById('prevtitle')

  var prevTitleElement = document.createElement('h4')
  var x = localStorage.getItem('pname');
  prevTitleElement.innerHTML = x;

  prevtitle.appendChild(prevTitleElement);

  document.getElementById('tool0').style.visibility = "visible"
  document.getElementById('tool1').style.visibility = "visible"
  document.getElementById('tool2').style.visibility = "visible"
  document.getElementById('starttool').remove()



}