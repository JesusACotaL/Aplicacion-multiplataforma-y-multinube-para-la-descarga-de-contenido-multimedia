import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SourceConfigModalComponent } from './source-config-modal.component';

describe('SourceConfigModalComponent', () => {
  let component: SourceConfigModalComponent;
  let fixture: ComponentFixture<SourceConfigModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SourceConfigModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SourceConfigModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
