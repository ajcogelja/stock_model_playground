import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChampInputAreaComponent } from './champ-input-area.component';

describe('ChampInputAreaComponent', () => {
  let component: ChampInputAreaComponent;
  let fixture: ComponentFixture<ChampInputAreaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ChampInputAreaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChampInputAreaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
