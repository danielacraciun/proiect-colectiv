from django import forms


class TemplateForm(forms.Form):
    docfile = forms.FileField(label='Select a file')

    def clean_file(self):
        file = self.cleaned_data['file']
        try:
            if file:
                file_type = file.content_type.split('/')[0]

                if len(file.name.split('.')) == 1:
                    raise forms.ValidationError(_('File type is not supported'))

                if file_type in settings.TASK_UPLOAD_FILE_TYPES:
                    if file._size > settings.TASK_UPLOAD_FILE_MAX_SIZE:
                        raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(file._size)))
                else:
                    raise forms.ValidationError(_('File type is not supported'))
        except:
            pass

        return file
