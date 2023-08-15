import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SiteConfigModalComponent } from './site-config-modal.component';

describe('SiteConfigModalComponent', () => {
  let component: SiteConfigModalComponent;
  let fixture: ComponentFixture<SiteConfigModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SiteConfigModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SiteConfigModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
