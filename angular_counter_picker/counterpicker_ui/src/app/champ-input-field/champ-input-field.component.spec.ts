import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChampInputFieldComponent } from './champ-input-field.component';

describe('ChampInputFieldComponent', () => {
  let component: ChampInputFieldComponent;
  let fixture: ComponentFixture<ChampInputFieldComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ChampInputFieldComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChampInputFieldComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
