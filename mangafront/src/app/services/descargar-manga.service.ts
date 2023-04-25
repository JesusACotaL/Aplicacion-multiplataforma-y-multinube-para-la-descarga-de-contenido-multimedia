import { Injectable } from '@angular/core';
import jsPDF from 'jspdf';

@Injectable({
  providedIn: 'root'
})
export class DescargarMangaService {
  constructor() {}
  ngOnInit() {}
  cargarImagenes(urls: string) {
    console.log('Preparando imagenes: '+urls);
    let imgs: Array<HTMLImageElement> = [];
    let fuentes = [];
    fuentes = urls.split("\n");
    for (const fuente of fuentes) {
      const img = new Image();
      img.src = fuente;
      imgs.push(img);
    }
    return imgs;
  }
  generarPDF(imagenes: Array<HTMLImageElement>) {
    console.log('Preparando pdf...');
    const pdf = new jsPDF({
      orientation: "portrait",
      unit: 'mm',
      format: 'letter'
    });
    for (const [i,img] of imagenes.entries()) {
      if(i > 0) pdf.addPage();
      pdf.addImage(img, 'JPEG', 0, 0, pdf.internal.pageSize.getWidth(),pdf.internal.pageSize.getHeight());
    }
    console.log('Descargando pdf...');
    pdf.save("manga.pdf");
  }
}
