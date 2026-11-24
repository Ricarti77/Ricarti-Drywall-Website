(function(){
var ON="background:#24272A;color:#FFFFFF;border:0;padding:14px 12px;font-family:inherit;font-size:15px;font-weight:500;cursor:pointer;min-height:48px";
var OFF="background:#FFFFFF;color:#24272A;border:0;padding:14px 12px;font-family:inherit;font-size:15px;font-weight:500;cursor:pointer;min-height:48px";
var who=/[?&]type=builder/.test(location.search)?"builder":"home", start="visit";
function show(k,v){document.querySelectorAll('[data-show="'+k+'"]').forEach(function(e){e.hidden=!v;});}
function syncFields(){document.querySelectorAll('#rd-form input,#rd-form select,#rd-form textarea').forEach(function(el){if(el.type==="hidden"||el.name==="_honey")return;el.disabled=!!el.closest('[hidden]');});}
function render(){
 var h=who==="home";
 show("home",h); show("builder",!h); show("visit",h&&start==="visit");
 var a=document.getElementById("rd-home"), b=document.getElementById("rd-builder");
 a.setAttribute("style",h?ON:OFF); b.setAttribute("style",h?OFF:ON);
 a.setAttribute("aria-pressed",h); b.setAttribute("aria-pressed",!h);
 document.getElementById("rd-upload").textContent=h?"PHOTOS OR PLANS (OPTIONAL)":"DRAWINGS (PDF)";
 document.getElementById("rd-notes").placeholder=h?"Ceiling heights, rooms that get strong light, paint you have in mind…":"Schedule, phase, site access, anything we should price around…";
 document.getElementById("rd-who").value=h?"Homeowner":"Builder / contractor";
 syncFields();
 document.getElementById("rd-submit").textContent=h?(start==="visit"?"Request a site visit":"Get a ballpark"):"Request pricing";
}
document.getElementById("rd-home").addEventListener("click",function(){who="home";render();});
document.getElementById("rd-builder").addEventListener("click",function(){who="builder";render();});
document.querySelectorAll('input[name="How to start"]').forEach(function(r){r.addEventListener("change",function(){start=r.value==="Site visit"?"visit":"photos";render();});});
document.getElementById("rd-form").addEventListener("submit",function(){
 var f=this,n=(f.Name&&f.Name.value)||"";
 document.getElementById("rd-subject").value=(who==="home"?(start==="visit"?"Site visit request":"Ballpark request"):"Builder pricing request")+" — "+n;
 document.getElementById("rd-next").value=location.origin+"/estimate?sent=1"+(who==="builder"?"&type=builder":"");
 syncFields();
});
if(/[?&]sent=1/.test(location.search)){show("form",false);show("sent",true);}
document.getElementById("rd-reset").addEventListener("click",function(){location.href="/estimate"+(who==="builder"?"?type=builder":"");});
render();
})();
