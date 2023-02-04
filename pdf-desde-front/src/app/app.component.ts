import { Component } from '@angular/core';
import { jsPDF } from "jspdf";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'pdf-desde-front';
  imgs: Array<HTMLImageElement> = [];
  constructor() {}
  ngOnInit() {}

  cargarImagenes() {
    let fuentes = [
      "assets/imagenesPrueba/output.jpg",
      "assets/imagenesPrueba/output2.jpg"
    ];
    for (const fuente of fuentes) {
      const img = new Image();
      img.src = fuente;
      this.imgs.push(img);
    }
  }

  generarPDF(imagenes: Array<HTMLImageElement>) {
    const pdf = new jsPDF({
      orientation: "portrait",
      unit: 'in',
      format: 'a4'
    });
    for (const [i,img] of imagenes.entries()) {
      if(i > 0) pdf.addPage();
      pdf.addImage(img, 'JPG', 0, 0, pdf.internal.pageSize.getWidth(),pdf.internal.pageSize.getHeight());
    }
    pdf.save("queso.pdf");
  }
}
