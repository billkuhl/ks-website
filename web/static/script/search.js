function search() {
    let input = document.getElementById('searchField');
    let filter = input.value.toUpperCase();
    li = document.getElementById('freshmen').getElementsByTagName('li');
    
    for (let i = 0; i < li.length; i++) {
        let object = li[i];
        let freshman = object.getElementsByTagName('b')[0];
        let name = freshman.textContent || freshman.innerText;

        if (name.toUpperCase().indexOf(filter) > -1){
            object.style.display = '';
        } else {
            object.style.display = 'none';
        }
    }
}