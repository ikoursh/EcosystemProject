const embed = document.getElementById('embed');
let menue_elements = document.getElementById('option_group').children;
let active = null;
for (var i = 0; i < menue_elements.length; i++) {
  menue_elements[i].addEventListener('click', function(){
    display(this.innerHTML.replace(" ", "_").toLowerCase()+".html")
    if (active!=null){
      active.className = null;
    }
    this.className = "active";
    active = this;
  });
}

menue_elements[0].click()


function display(page) {
  console.log(page);
  embed.src = "./pages/"+page;
}
