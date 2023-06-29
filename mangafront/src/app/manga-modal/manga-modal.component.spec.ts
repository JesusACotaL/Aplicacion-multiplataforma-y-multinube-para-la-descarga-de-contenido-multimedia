import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MangaModalComponent } from './manga-modal.component';

describe('MangaModalComponent', () => {
  let component: MangaModalComponent;
  let fixture: ComponentFixture<MangaModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MangaModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MangaModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
