import { HttpClient, HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { JsonFetcherService } from './json-fetcher.service';
import { MatSelectModule } from '@angular/material/select';
import { MatOptionModule } from '@angular/material/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import { MaterialExampleModule } from './material.module';
import { ChampInputFieldComponent } from './champ-input-field/champ-input-field.component';
import { ChampInputAreaComponent } from './champ-input-area/champ-input-area.component';


@NgModule({
  declarations: [
    AppComponent,
    ChampInputFieldComponent,
    ChampInputAreaComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatSelectModule,
    MatOptionModule,
    MatFormFieldModule,
    MatAutocompleteModule,
    FormsModule,
    ReactiveFormsModule,
    MatInputModule,
    MaterialExampleModule,
    HttpClientModule
  ],
  providers: [JsonFetcherService],
  bootstrap: [AppComponent]
})
export class AppModule { }
