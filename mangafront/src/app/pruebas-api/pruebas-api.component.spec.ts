import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PruebasAPIComponent } from './pruebas-api.component';

describe('PruebasAPIComponent', () => {
  let component: PruebasAPIComponent;
  let fixture: ComponentFixture<PruebasAPIComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PruebasAPIComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PruebasAPIComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
