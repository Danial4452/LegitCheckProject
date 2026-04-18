import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api'; 
import { Product } from '../../models/product';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-result',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './result.html',
  styleUrl: './result.scss'
})
export class ResultComponent implements OnInit {
  product: Product | null = null;
  error: string | null = null;
  loading: boolean = true;

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    const code = this.route.snapshot.paramMap.get('code');
    this.loading = true;

    setTimeout(() => {
      // Имитация логики: если в коде есть слово "fake", то это подделка
      const isFake = code?.toLowerCase().includes('fake');

      this.product = {
        id: 1,
        name: isFake ? "Unknown Model (Suspicious)" : "Air Jordan 1 Retro High",
        brand: isFake ? "Replica" : "Nike",
        is_authentic: !isFake, 
        serial_number: code || 'DEMO-123', 
        manufacture_location: isFake ? "Non-official workshop" : "Vietnam, Factory PH-04",
        history: isFake 
          ? "ВНИМАНИЕ: Данный серийный номер совпадает с известными копиями или не прошел проверку материалов." 
          : "Данная пара успешно прошла автоматизированную проверку в базе KBTU."
      };
      
      this.loading = false;
      this.cdr.detectChanges(); 
    }, 1500); 
  }
}