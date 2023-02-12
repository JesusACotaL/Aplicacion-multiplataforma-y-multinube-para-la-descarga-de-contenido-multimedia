import { Component } from '@angular/core';
import { jsPDF } from "jspdf";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'pdf-desde-front';
  fuentes = "";
  imgs: Array<HTMLImageElement> = [];
  constructor() {}
  ngOnInit() {}

  cargarImagenes(urls: string) {
    this.imgs = [];
    let fuentes = [];
    fuentes = urls.split("\n");
    for (const fuente of fuentes) {
      const img = new Image();
      img.src = fuente;
      this.imgs.push(img);
    }
  }

  generarPDF(imagenes: Array<HTMLImageElement>) {
    const pdf = new jsPDF({
      orientation: "portrait",
      unit: 'mm',
      format: 'letter'
    });
    for (const [i,img] of imagenes.entries()) {
      if(i > 0) pdf.addPage();
      pdf.addImage(img, 'JPEG', 0, 0, pdf.internal.pageSize.getWidth(),pdf.internal.pageSize.getHeight());
    }
    pdf.save("queso.pdf");
  }
}
