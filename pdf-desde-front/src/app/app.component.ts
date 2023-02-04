import { Component } from '@angular/core';
import { jsPDF } from "jspdf";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'pdf-desde-front';
  constructor() {}
  ngOnInit() {}

  generarPDF() {
    const doc = new jsPDF({
      orientation: "landscape",
      unit: "in",
      format: [4, 2]
    });
    doc.text("Hello world!", 10, 10);
    doc.save("a4.pdf");
  }
}
