document.addEventListener('DOMContentLoaded',function(){
    const selectBtns = document.querySelectorAll('.song-select-btn');

    selectBtns.forEach(button =>{
        button.addEventListener('click',function(){
            const songId = this.getAttribute('data-song-id');
            const checkbox = this.parentElement.querySelector('.song-checkbox');

            this.classList.toggle('selected');
            checkbox.checked= !checkbox.checked;

                        
        })
    })

})