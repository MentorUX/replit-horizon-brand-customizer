document.addEventListener('DOMContentLoaded', (event) => {
    const previewButton = document.getElementById('previewButton');
    const previewCompanyName = document.getElementById('preview-company-name');
    const previewLogo = document.getElementById('preview-logo');
    const previewHeader = document.getElementById('preview-header');
    const previewContent = document.getElementById('preview-content');

    // Company Name
    const companyNameInput = document.getElementById('company_name');
    companyNameInput.addEventListener('input', function() {
        previewCompanyName.textContent = this.value;
    });

    // Logo
    const logoInput = document.getElementById('logo-input');
    const deleteLogoButton = document.getElementById('delete-logo');

    function updateLogoDisplay(logoUrl) {
        const logoPreview = document.getElementById('logo-preview');
        const logoInputContainer = document.getElementById('logo-input-container');

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
            // Update preview
            previewLogo.src = logoUrl;
            previewLogo.style.display = 'block';
        } else {
            if (logoPreview) {
                logoPreview.remove();
            }
            logoInputContainer.style.display = 'block';
            if (deleteLogoButton) {
                deleteLogoButton.style.display = 'none';
            }
            // Update preview
            previewLogo.style.display = 'none';
        }
    }

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

    // Colors and Button Radius
    const colorInputs = [
        { picker: 'brand_color_picker', input: 'brand_color', previewElement: 'preview-content' },
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

    // Button radius
    const radiusInput = document.getElementById('button_radius');
    const radiusValue = document.getElementById('radiusValue');

    if (radiusInput && previewButton && radiusValue) {
        radiusInput.addEventListener('input', function() {
            previewButton.style.borderRadius = `${this.value}px`;
            radiusValue.textContent = this.value;
        });

        // Set initial value
        radiusValue.textContent = radiusInput.value;
        previewButton.style.borderRadius = `${radiusInput.value}px`;
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

    // Set initial preview values
    if (companyNameInput) {
        previewCompanyName.textContent = companyNameInput.value;
    }

    if (previewLogo && logoInput) {
        const currentLogo = document.getElementById('logo-preview');
        if (currentLogo) {
            previewLogo.src = currentLogo.src;
            previewLogo.style.display = 'block';
        }
    }

    // Trigger initial preview updates
    colorInputs.forEach(({ input }) => {
        const inputElement = document.getElementById(input);
        if (inputElement) {
            inputElement.dispatchEvent(new Event('input'));
        }
    });
});
