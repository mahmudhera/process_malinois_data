import pandas as pd

def main():
    # read media-4.xlsx file
    df_media4 = pd.read_excel('media-4.xlsx')
    variant_list_with_mpra_readout = df_media4['variant'].tolist()
    log2_skew_HEPG2 = df_media4['log2Skew_HEPG2'].tolist()
    log2_skew_K562 = df_media4['log2Skew_K562'].tolist()
    log2_skew_SKNSH = df_media4['log2Skew_SKNSH'].tolist()
    variant_to_skew = {}
    num_variants_with_problem = 0
    for variant, skew_hepg2, skew_k562, skew_skNSH in zip(variant_list_with_mpra_readout, log2_skew_HEPG2, log2_skew_K562, log2_skew_SKNSH):
        variant_to_skew[variant] = (skew_k562, skew_hepg2, skew_skNSH)
        
    print(f"Number of variants with MPRA readout: {len(variant_to_skew)}")
    print(f"Number of variants with problem in MPRA readout: {num_variants_with_problem}")

    # read media-3.xlsx file
    df = pd.read_excel('media-3.xlsx')
    
    # get the list of variants
    variant_list = df['Variant'].tolist()
    allele1_seq = df['Allele 1 Oligo'].tolist()
    allele2_seq = df['Allele 2 Oligo'].tolist()

    num_snp_variants = 0
    found_in_list_of_variants_with_mpra_readout = 0
    rows = []
    for variant, allele1, allele2 in zip(variant_list, allele1_seq, allele2_seq):
        if len(allele1) == 200 and len(allele2) == 200:
            num_snp_variants += 1
            if variant in variant_to_skew:
                found_in_list_of_variants_with_mpra_readout += 1
                skew_k562, skew_hepg2, skew_skNSH = variant_to_skew[variant]
                rows.append({'variant': variant, 'ref_seq': allele1, 'alt_seq': allele2, 'log2_skew_k562': skew_k562, 'log2_skew_HEPG2': skew_hepg2, 'log2_skew_SKNSH': skew_skNSH})

    print(f"Total number of variants: {len(variant_list)}")
    print(f"Number of SNP variants: {num_snp_variants}")
    print(f"Number of SNP variants found in list of variants with MPRA readout: {found_in_list_of_variants_with_mpra_readout}")

    # save the output dataframe to a tsv file
    output_df = pd.DataFrame(rows)
    output_df.to_csv('mpac_paper_data_processed.tsv', sep='\t', index=False)
    

if __name__ == "__main__":
    main()