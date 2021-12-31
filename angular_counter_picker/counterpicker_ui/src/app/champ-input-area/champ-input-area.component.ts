import { Component, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ChampInputFieldComponent } from '../champ-input-field/champ-input-field.component';
import { JsonFetcherService } from '../json-fetcher.service';

@Component({
  selector: 'app-champ-input-area',
  templateUrl: './champ-input-area.component.html',
  styleUrls: ['./champ-input-area.component.scss']
})
export class ChampInputAreaComponent implements AfterViewInit {


  Roles = Roles
  constructor(private fetcher: JsonFetcherService) { }
  @ViewChild('top') topChamp: ChampInputFieldComponent;
  @ViewChild('mid') midChamp: ChampInputFieldComponent;

  pressListener = (event: any) =>{
    console.log('top champ: ', this.topChamp)
    console.log('value: ', this.topChamp.getValue())
    //this.fetcher.getChampData(this.topChamp.getValue());
  }
  
  ngAfterViewInit(): void {
  //  const list = document.querySelector('app-champ-input-field') 
  // list!.addEventListener('keypress', this.pressListener)
   const checkButton = document.querySelector('button');
   console.log(checkButton);
   checkButton!.addEventListener('click', this.checkCounters)
  }

  checkCounters = () => {
    console.log(this.fetcher.getChampData(this.topChamp.getValue()))
  }


}

export enum Roles {
  Top='top',
  Jg='jg',
  Mid='mid',
  Bot='bot',
  Sup='sup'
}