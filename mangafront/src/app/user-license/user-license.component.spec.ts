import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserLicenseComponent } from './user-license.component';

describe('UserLicenseComponent', () => {
  let component: UserLicenseComponent;
  let fixture: ComponentFixture<UserLicenseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UserLicenseComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UserLicenseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
