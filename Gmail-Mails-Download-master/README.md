# Gmail-Mails-Download
Download all mails from gmail and save to pc

First of all, I would like to thank these passive contributors. I used their resources to build this.
1) [abjennings](https://github.com/abjennings/gmail-backup)
2) [Armand Niculescu](http://www.media-division.com/using-python-to-batch-rename-email-files/)
3) [nickrussler](https://github.com/nickrussler/eml-to-pdf-converter)
4) [wkhtmltopdf](https://github.com/wkhtmltopdf/wkhtmltopdf)

Quick start:

`docker run --rm -it -v /tmp/.X11-unix:/tmp/.X11-unix:ro -e DISPLAY=$DISPLAY  -v "{inser_path_to_save_on_pc}":/src/emails_backup --name gmailpdf projectarmstrong/gmail-mails-downloader-pdf`

Will add deatiled read me soon.
