//Ver bien esto, que está incompleto
document.querySelectorAll('input[name="tipo"]').forEach(radio => {
    radio.addEventListener('change', e => {
        document.getElementById('campoCUIG').style.display = 
            e.target.value === 'senasa' ? 'block' : 'none';
    });
});