document.addEventListener('DOMContentLoaded', (event) => {
    // Preview button radius change
    const radiusInput = document.getElementById('button_radius');
    const previewButton = document.getElementById('previewButton');
    const radiusValue = document.getElementById('radiusValue');

    if (radiusInput && previewButton && radiusValue) {
        radiusInput.addEventListener('input', function() {
            previewButton.style.borderRadius = `${this.value}px`;
            radiusValue.textContent = this.value;
        });

        // Set initial value
        radiusValue.textContent = radiusInput.value;
    }

    // Preview color changes
    const colorInputs = [
        { picker: 'brand_color_picker', input: 'brand_color', previewElement: 'preview' },
        { picker: 'button_bg_color_picker', input: 'button_bg_color', previewElement: 'previewButton' },
        { picker: 'button_text_color_picker', input: 'button_text_color', previewElement: 'previewButton' },
        { picker: 'button_hover_bg_color_picker', input: 'button_hover_bg_color', previewElement: 'previewButton' },
        { picker: 'button_hover_text_color_picker', input: 'button_hover_text_color', previewElement: 'previewButton' }
    ];

    colorInputs.forEach(({ picker, input, previewElement }) => {
        const pickerElement = document.getElementById(picker);
        const inputElement = document.getElementById(input);
        const previewEl = document.getElementById(previewElement);

        if (pickerElement && inputElement && previewEl) {
            const updatePreview = () => {
                const color = inputElement.value;
                if (input === 'brand_color') {
                    previewEl.style.backgroundColor = color;
                } else if (input === 'button_bg_color') {
                    previewEl.style.backgroundColor = color;
                } else if (input === 'button_text_color') {
                    previewEl.style.color = color;
                } else if (input === 'button_hover_bg_color') {
                    previewEl.dataset.hoverBgColor = color;
                } else if (input === 'button_hover_text_color') {
                    previewEl.dataset.hoverTextColor = color;
                }
            };

            pickerElement.addEventListener('input', function() {
                inputElement.value = this.value;
                updatePreview();
            });

            inputElement.addEventListener('input', function() {
                pickerElement.value = this.value;
                updatePreview();
            });

            // Set initial values
            pickerElement.value = inputElement.value;
            updatePreview();
        }
    });

    // Update logo preview and input visibility
    function updateLogoDisplay(logoUrl) {
        const logoPreview = document.getElementById('logo-preview');
        const logoInputContainer = document.getElementById('logo-input-container');
        const deleteLogoButton = document.getElementById('delete-logo');

        if (logoUrl) {
            if (logoPreview) {
                logoPreview.src = logoUrl;
                logoPreview.style.display = 'block';
            } else {
                const newLogoPreview = document.createElement('img');
                newLogoPreview.id = 'logo-preview';
                newLogoPreview.src = logoUrl;
                newLogoPreview.alt = 'Company Logo';
                newLogoPreview.className = 'mb-2 max-w-full h-auto';
                document.getElementById('logo-container').insertBefore(newLogoPreview, logoInputContainer);
            }
            logoInputContainer.style.display = 'none';
            if (deleteLogoButton) {
                deleteLogoButton.style.display = 'block';
            }
        } else {
            if (logoPreview) {
                logoPreview.remove();
            }
            logoInputContainer.style.display = 'block';
            if (deleteLogoButton) {
                deleteLogoButton.style.display = 'none';
            }
        }
    }

    // Logo preview and deletion
    const logoInput = document.getElementById('logo-input');
    const deleteLogoButton = document.getElementById('delete-logo');

    if (logoInput) {
        logoInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    updateLogoDisplay(e.target.result);
                };
                reader.readAsDataURL(file);
            }
        });
    }

    if (deleteLogoButton) {
        deleteLogoButton.addEventListener('click', function() {
            fetch('/delete_logo', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateLogoDisplay(null);
                } else {
                    console.error('Error deleting logo:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    // Button hover state preview
    if (previewButton) {
        previewButton.addEventListener('mouseenter', function() {
            this.style.backgroundColor = this.dataset.hoverBgColor;
            this.style.color = this.dataset.hoverTextColor;
        });

        previewButton.addEventListener('mouseleave', function() {
            this.style.backgroundColor = document.getElementById('button_bg_color').value;
            this.style.color = document.getElementById('button_text_color').value;
        });
    }
});
