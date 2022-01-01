import { Component, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ChampInputFieldComponent } from '../champ-input-field/champ-input-field.component';
import { JsonFetcherService } from '../json-fetcher.service';

@Component({
  selector: 'app-champ-input-area',
  templateUrl: './champ-input-area.component.html',
  styleUrls: ['./champ-input-area.component.scss']
})
export class ChampInputAreaComponent implements AfterViewInit {

  counters: string[] = []
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
    const data = this.fetcher.getChampData(this.topChamp.getValue())
    const data2 = this.fetcher.getChampData(this.midChamp.getValue())
    this.counters = []
    const counters1: string[] = []
    const counters2: string[] = []
    if(data !== null){
    //this.counters = []
      Object.keys(data.counters).forEach(element => { //get position
        Object.keys(data.counters[element]).forEach(i => {
          //console.log('i1: ', i);
          if(!counters1.includes(i)){
            counters1.push(i)
          }
        })
      });
    }
    if(data2 !== null){
      Object.keys(data2.counters).forEach(element => { //get position
        Object.keys(data2.counters[element]).forEach(i => {
          //console.log('i2: ', i);
          if(!counters2.includes(i)){
            counters2.push(i)
          }
        })
      });
    }
    if(counters1.length > 0 && counters2.length > 0){
      for(const c of counters1){
        if(counters2.includes(c)){
          //console.log('both lists have: ', c);
          this.counters.push(c);
        }
      }
    }
    console.log()

  }

  clearCounters = () => {

  }


}

export enum Roles {
  Top='top',
  Jg='jg',
  Mid='mid',
  Bot='bot',
  Sup='sup'
}