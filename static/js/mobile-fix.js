(function(){
var h=document.getElementById('hamburger');
var s=document.querySelector('.sidebar');
var o=document.getElementById('sidebarOverlay');
if(h&&s){h.addEventListener('click',function(){h.classList.toggle('active');s.classList.toggle('active');if(o)o.classList.toggle('active')})}
if(o){o.addEventListener('click',function(){if(h)h.classList.remove('active');if(s)s.classList.remove('active');o.classList.remove('active')})}
document.querySelectorAll('input[type="password"]').forEach(function(input){
if(input.getAttribute('data-pw-fixed'))return;
input.setAttribute('data-pw-fixed','1');
var wrap=document.createElement('div');
wrap.className='pw-wrap';
input.parentNode.insertBefore(wrap,input);
wrap.appendChild(input);
var btn=document.createElement('button');
btn.type='button';
btn.className='pw-toggle';
btn.innerHTML='&#128065;';
btn.onclick=function(e){
e.preventDefault();
if(input.type==='password'){input.type='text';btn.innerHTML='&#128584;'}
else{input.type='password';btn.innerHTML='&#128065;'}
};
wrap.appendChild(btn);
});
})();
