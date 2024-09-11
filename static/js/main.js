document.addEventListener('DOMContentLoaded', (event) => {
    const previewButton = document.getElementById('previewButton');
    const previewButton2 = document.getElementById('previewButton2');
    const radiusInput = document.getElementById('button_radius');
    const radiusValue = document.getElementById('radiusValue');
    const companyNameInput = document.getElementById('company_name');
    const companyNamePreview = document.getElementById('company-name-preview');
    const logoInput = document.getElementById('logo-input');
    const logoPreviewImage = document.getElementById('logo-preview-image');
    const logoPreviewContainer = document.getElementById('logo-preview-container');
    const deleteLogoButton = document.getElementById('delete-logo');
    const preview = document.getElementById('preview');
    const previewHeader = preview.querySelector('header');
    const previewFooter = preview.querySelector('footer');

    const colorInputs = [
        { picker: 'brand_color_picker', input: 'brand_color', previewElement: 'preview' },
        { picker: 'button_primary_default_color_bg_picker', input: 'button_primary_default_color_bg', previewElement: 'previewButton' },
        { picker: 'button_primary_default_color_text_picker', input: 'button_primary_default_color_text', previewElement: 'previewButton' },
        { picker: 'button_primary_default_color_stroke_picker', input: 'button_primary_default_color_stroke', previewElement: 'previewButton' },
        { picker: 'button_primary_hover_color_bg_picker', input: 'button_primary_hover_color_bg', previewElement: 'previewButton' },
        { picker: 'button_primary_hover_color_text_picker', input: 'button_primary_hover_color_text', previewElement: 'previewButton' },
        { picker: 'button_primary_hover_color_stroke_picker', input: 'button_primary_hover_color_stroke', previewElement: 'previewButton' }
    ];

    function updatePreview() {
        const brandColor = document.getElementById('brand_color').value;

        // Update company name and header
        companyNamePreview.textContent = companyNameInput.value;
        companyNamePreview.style.backgroundColor = brandColor;
        companyNamePreview.style.color = '#ffffff'; // White text
        companyNamePreview.style.padding = '10px';
        companyNamePreview.style.width = '100%';

        // Update footer
        previewFooter.style.backgroundColor = brandColor;
        previewFooter.style.color = '#ffffff'; // White text
        previewFooter.querySelector('p').textContent = `© 2024 ${companyNameInput.value}. All rights reserved.`;

        // Set a neutral background color for the preview section
        preview.style.backgroundColor = '#f0f0f0'; // Light gray background

        // Update button styles
        const buttonStyle = {
            backgroundColor: document.getElementById('button_primary_default_color_bg').value,
            color: document.getElementById('button_primary_default_color_text').value,
            borderColor: document.getElementById('button_primary_default_color_stroke').value,
            borderWidth: '2px',
            borderStyle: 'solid',
            borderRadius: `${radiusInput.value}px`
        };

        [previewButton, previewButton2].forEach(button => {
            Object.assign(button.style, buttonStyle);
        });

        // Update hover states
        const hoverStyle = {
            hoverBgColor: document.getElementById('button_primary_hover_color_bg').value,
            hoverTextColor: document.getElementById('button_primary_hover_color_text').value,
            hoverStrokeColor: document.getElementById('button_primary_hover_color_stroke').value
        };

        [previewButton, previewButton2].forEach(button => {
            button.dataset.hoverBgColor = hoverStyle.hoverBgColor;
            button.dataset.hoverTextColor = hoverStyle.hoverTextColor;
            button.dataset.hoverStrokeColor = hoverStyle.hoverStrokeColor;
        });
    }

    // Initialize preview
    updatePreview();

    // Company name live update
    companyNameInput.addEventListener('input', updatePreview);

    // Button radius live update
    if (radiusInput && previewButton && radiusValue) {
        radiusInput.addEventListener('input', function() {
            updatePreview();
            radiusValue.textContent = this.value;
        });

        // Set initial value
        radiusValue.textContent = radiusInput.value;
    }

    // Color inputs live update
    colorInputs.forEach(({ picker, input, previewElement }) => {
        const pickerElement = document.getElementById(picker);
        const inputElement = document.getElementById(input);
        const previewEl = previewElement ? document.getElementById(previewElement) : null;

        if (pickerElement && inputElement) {
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
        }
    });

    // Logo preview
    if (logoInput) {
        logoInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    logoPreviewImage.src = e.target.result;
                    logoPreviewImage.classList.remove('hidden');
                    logoPreviewContainer.classList.remove('hidden');
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Delete logo
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
                    logoPreviewImage.src = '';
                    logoPreviewImage.classList.add('hidden');
                    logoPreviewContainer.classList.add('hidden');
                    logoInput.value = '';
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
    [previewButton, previewButton2].forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.backgroundColor = this.dataset.hoverBgColor;
            this.style.color = this.dataset.hoverTextColor;
            this.style.borderColor = this.dataset.hoverStrokeColor;
        });

        button.addEventListener('mouseleave', function() {
            this.style.backgroundColor = document.getElementById('button_primary_default_color_bg').value;
            this.style.color = document.getElementById('button_primary_default_color_text').value;
            this.style.borderColor = document.getElementById('button_primary_default_color_stroke').value;
        });
    });
});
