const links = document.querySelectorAll('a');

links.forEach(link => {
  link.addEventListener('click',()=>{
    // link.classList.add('active')

    // if(link.classList.contains('active')){
    //   link.classList.remove('active')
    // }

    console.log('click')
  })
});