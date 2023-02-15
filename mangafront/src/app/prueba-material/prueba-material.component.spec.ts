import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PruebaMaterialComponent } from './prueba-material.component';

describe('PruebaMaterialComponent', () => {
  let component: PruebaMaterialComponent;
  let fixture: ComponentFixture<PruebaMaterialComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PruebaMaterialComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PruebaMaterialComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
