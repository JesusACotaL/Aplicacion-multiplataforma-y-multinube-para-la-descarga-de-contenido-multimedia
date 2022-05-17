import { HttpClient, HttpParams } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';

export interface Capitulo{
  Nombre: string,
  Url: string
}

@Component({
  selector: 'app-mangaka',
  templateUrl: './mangaka.component.html',
  styleUrls: ['./mangaka.component.css']
})

export class MangakaComponent implements OnInit {
  capitulos: Capitulo[]=[]
  mangaName : string | null="";
  author : string | null = "";
  stars : string | null = "";
  chapter_url : string | null = "";
  image_url : string | null = "";
  headers : any ;

  constructor(
    private activatedRoute:ActivatedRoute,
    private http : HttpClient
  ) { 
    this.activatedRoute.paramMap.subscribe(
      (data) => {
        this.mangaName = data.get('name')
      }
    ) 
    this.headers = {'Access-Control-Allow-Headers':'*','Access-Control-Allow-Origin':'*',
    'Content-Type': 'application/json','Access-Control-Allow-Methods':'OPTIONS, POST, GET',
    'Referrer-Policy':'strict-origin-when-cross-origin'};
  }

  get_manga_chapters(): Observable<any>{
    const headers = this.headers;
    const body = { url: this.chapter_url };
    let url = "https://5t9ckx5fk5.execute-api.us-west-1.amazonaws.com/final/get-manga-chapters"
    return this.http.post<any>(url,body,{headers});
  }

  get_manga_info(): Observable<any>{
    const headers = this.headers
    let re = /\ /gi;
    let nombre = this.mangaName?.replace(re,"_");
    const body = {url:'https://m.manganelo.com/search/story/'+`${nombre}`}
    let url = "https://5t9ckx5fk5.execute-api.us-west-1.amazonaws.com/final/get-manga-info"
    return this.http.post<any>(url,body,{headers});
  }

  get_chapter_links(urls:string[]): void {
    const headers = this.headers
    let https = this.http;
    let url = "https://5t9ckx5fk5.execute-api.us-west-1.amazonaws.com/final/get-manga-urls";
    urls.forEach(function(item){
      const body = {url:item}
      let chapter_images_urls = https.post<any>(url,body,{headers});
      chapter_images_urls.subscribe(
        (data)=>{
          console.log(data) //links de las imagenes
          let pdfname = ((document.getElementById("pdfName") as HTMLInputElement).value);
          const body2 = {format:"pdf",book_name:pdfname,images_urls:data}
          let url2 = "https://5t9ckx5fk5.execute-api.us-west-1.amazonaws.com/v8/get-manga-file"
          https.post<any>(url2,body2,{headers}).subscribe(response=>{
            console.log(response)
            let urldownload= response.body.file_url;
            https.get(urldownload,{headers, responseType: 'blob' as 'json'}).subscribe(
              (response: any) =>{
                  let dataType = response.type;
                  let binaryData = [];
                  binaryData.push(response);
                  let downloadLink = document.createElement('a');
                  downloadLink.href = window.URL.createObjectURL(new Blob(binaryData, {type: dataType}));
                  if (pdfname)
                      downloadLink.setAttribute('download', pdfname+".pdf");
                  document.body.appendChild(downloadLink);
                  downloadLink.click();
              }
            )
          })
        }
      );
    });
  }

  ngOnInit(): void { 
    this.get_manga_info().subscribe(
      (data)=>{
        this.mangaName = data[0].name
        this.author = data[0].author
        this.stars = data[0].stars
        this.chapter_url = data[0].chapters_url
        this.image_url = data[0].image_url
        this.get_manga_chapters().subscribe(
          (data)=>{
            this.capitulos = data.body;
            this.capitulos = this.capitulos.reverse()
          }
        )
      }
    )
    
  }

  download_chapters():void{
    let rango = ((document.getElementById("chapterRange") as HTMLInputElement).value);
    let inicia = parseInt(rango.split('-')[0])
    let final = parseInt(rango.split('-')[1])
    let urls : string [] = [];
    for (let i = inicia; i <=final; i++){
      urls.push(this.capitulos[i-1].Url)
    }
    this.get_chapter_links(urls)
  }

}



