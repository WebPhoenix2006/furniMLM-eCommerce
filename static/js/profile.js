const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach((button,index) => {
  button.addEventListener('click',()=>{
    tabContents.forEach((content)=>{
      content.classList.remove('active')
    })

    tabContents[index].classList.add('active');

    tabButtons.forEach((btn)=>{
      btn.classList.remove('active')
    })

    button.classList.add('active')
  })
})