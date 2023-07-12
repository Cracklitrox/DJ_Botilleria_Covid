const input = document.querySelector('input[type="file"]');
const imagePreview = document.getElementById('imagePreview');
const existingImage = document.querySelector('.existing-image img');

input.addEventListener('change', function (event) {
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();

        reader.addEventListener('load', function () {
            const image = new Image();
            image.src = this.result;
            imagePreview.innerHTML = '';
            imagePreview.appendChild(image);

            if (existingImage) {
                existingImage.style.display = 'none';
            }
        });

        reader.readAsDataURL(file);
    } else {
        imagePreview.innerHTML = '';

        if (existingImage) {
            existingImage.style.display = 'block';
        }
    }
});

if (existingImage) {
    const image = new Image();
    image.src = existingImage.src;
    imagePreview.innerHTML = '';
    imagePreview.appendChild(image);

    existingImage.style.display = 'none';
}